from flask import Flask, jsonify, request
from recommendation_model import model

app = Flask(__name__)

@app.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    """
    Returns product recommendations for a given user ID.
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user to get recommendations for.
      - name: n
        in: query
        type: integer
        required: false
        default: 5
        description: Number of recommendations to return.
    """
    try:
        num_recs = int(request.args.get('n', 5))
        recommendations = model.get_recommendations(user_id, num_recs=num_recs)
        
        if not recommendations:
            return jsonify({'message': 'No recommendations found for this user.', 'recommendations': []}), 404

        return jsonify({'user_id': user_id, 'recommendations': recommendations})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # When running locally, the model is already trained upon import.
    app.run(debug=True, port=5001)