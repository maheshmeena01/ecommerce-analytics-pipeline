import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

# --- Database Connection ---
# Use the same DB_URL as in the ETL script
DB_URL = "postgresql://postgres:admin@localhost:5432/ecommerce_db"

class RecommendationEngine:
    def __init__(self):
        self.engine = create_engine(DB_URL)
        self.user_item_matrix = None
        self.user_similarity_df = None
        self.user_map = None
        self.user_inv_map = None
        self.train_model()

    def train_model(self):
        """Fetches data and builds the user similarity matrix."""
        # Fetch interaction data
        query = "SELECT user_id, product_id, event_type FROM interactions"
        df = pd.read_sql(query, self.engine)

        # Simple weighting: purchase > add_to_cart > view
        event_weights = {'view': 1, 'add_to_cart': 2, 'purchase': 3}
        df['rating'] = df['event_type'].map(event_weights)
        
        # Aggregate ratings in case of multiple interactions
        df = df.groupby(['user_id', 'product_id'])['rating'].sum().reset_index()

        if df.empty:
            print("Not enough data to train the model.")
            return

        # Create user-item matrix
        self.user_map = {user_id: i for i, user_id in enumerate(df.user_id.unique())}
        self.user_inv_map = {i: user_id for user_id, i in self.user_map.items()}
        product_map = {prod_id: i for i, prod_id in enumerate(df.product_id.unique())}

        df['user_idx'] = df['user_id'].map(self.user_map)
        df['product_idx'] = df['product_id'].map(product_map)

        sparse_matrix = csr_matrix((df.rating, (df.user_idx, df.product_idx)))
        self.user_item_matrix = pd.DataFrame(sparse_matrix.toarray())

        # Calculate cosine similarity between users
        user_similarity = cosine_similarity(self.user_item_matrix)
        self.user_similarity_df = pd.DataFrame(user_similarity, index=self.user_item_matrix.index, columns=self.user_item_matrix.index)

        print("Recommendation model trained successfully.")

    def get_recommendations(self, user_id, num_recs=5):
        """Gets product recommendations for a given user."""
        if self.user_item_matrix is None or user_id not in self.user_map:
            # Return random popular products as a fallback
            print(f"User {user_id} not found or model not trained. Returning popular products.")
            popular_query = """
                SELECT p.product_id, p.name FROM interactions i
                JOIN products p ON i.product_id = p.product_id
                WHERE i.event_type = 'purchase'
                GROUP BY p.product_id, p.name
                ORDER BY COUNT(*) DESC LIMIT %s
            """
            popular_products = pd.read_sql(popular_query, self.engine, params=(num_recs,))
            return popular_products.to_dict('records')

        user_idx = self.user_map[user_id]
        
        # Get top 5 most similar users
        similar_users = self.user_similarity_df[user_idx].sort_values(ascending=False)[1:6]

        # Get products liked by similar users
        similar_user_products = self.user_item_matrix.iloc[similar_users.index]

        # Recommend products that the target user hasn't interacted with yet
        recommendations = similar_user_products.sum(axis=0).sort_values(ascending=False)
        user_interacted_products = self.user_item_matrix.iloc[user_idx]
        recommendations = recommendations[user_interacted_products == 0]

        # Map product indices back to product IDs
        product_inv_map = {i: prod_id for prod_id, i in pd.read_sql("SELECT DISTINCT product_id FROM interactions", self.engine)['product_id'].reset_index().set_index('product_id')['index'].items()}
        
        top_product_indices = recommendations.head(num_recs).index
        recommended_product_ids = [product_inv_map.get(idx) for idx in top_product_indices]
        
        # Fetch product details from DB
        if not recommended_product_ids:
            return []
            
        rec_query = "SELECT product_id, name, category, price FROM products WHERE product_id IN %s"
        recommended_products = pd.read_sql(rec_query, self.engine, params=(tuple(recommended_product_ids),))

        return recommended_products.to_dict('records')

# Instantiate the model globally so it's trained only once when the app starts
model = RecommendationEngine()
