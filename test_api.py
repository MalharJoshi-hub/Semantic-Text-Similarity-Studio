"""
Comprehensive automated tests for Semantic Similarity API and Engine.
"""

import unittest
import json
from app import app
import database
from engine import similarity_index

class TestSimilaritySystem(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        database.init_db()
        database.clear_all()
        similarity_index.rebuild_from_db()

    def test_01_stats_endpoint(self):
        res = self.client.get('/api/stats')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('corpus', data)
        self.assertIn('engine', data)

    def test_02_pair_similarity(self):
        # 1. Identical text -> 1.0
        res = self.client.post('/api/similarity/pair', json={
            "text1": "Machine learning enables computers to learn from data.",
            "text2": "Machine learning enables computers to learn from data."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertAlmostEqual(data['score'], 1.0, places=3)
        self.assertEqual(data['label'], 'Extremely High Similarity')

        # 2. Strong paraphrase -> > 0.80
        res2 = self.client.post('/api/similarity/pair', json={
            "text1": "The quick brown fox jumps over the lazy dog.",
            "text2": "A fast brown fox leaps over a sleepy canine."
        })
        self.assertEqual(res2.status_code, 200)
        data2 = res2.get_json()
        self.assertGreater(data2['score'], 0.80)
        self.assertIn('High Similarity', data2['label'])

        # 3. Unrelated text -> < 0.30
        res3 = self.client.post('/api/similarity/pair', json={
            "text1": "Astrophysicists study galaxies and gravitational waves.",
            "text2": "The sourdough bread should bake at 450 degrees Fahrenheit."
        })
        self.assertEqual(res3.status_code, 200)
        data3 = res3.get_json()
        self.assertLess(data3['score'], 0.30)
        self.assertEqual(data3['label'], 'Unrelated / Distinct')

        # 4. Input validation: missing fields
        res_err = self.client.post('/api/similarity/pair', json={"text1": ""})
        self.assertEqual(res_err.status_code, 400)

    def test_03_corpus_crud_and_query(self):
        # Add doc 1
        res = self.client.post('/api/texts', json={
            "label": "Deep Learning Guide",
            "content": "# Neural Networks\nDeep learning uses layered neural networks to process representations and extract hierarchical features.\n\n# Backpropagation\nBackpropagation computes gradients using the chain rule for numerical optimization."
        })
        self.assertEqual(res.status_code, 201)
        doc1 = res.get_json()['document']
        doc1_id = doc1['id']

        # Add doc 2
        res2 = self.client.post('/api/texts', json={
            "label": "Culinary Baking",
            "content": "# Sourdough Preparation\nFerment flour and water with wild yeast cultures over 24 hours to bake crusty bread."
        })
        self.assertEqual(res2.status_code, 201)
        doc2_id = res2.get_json()['document']['id']

        # Query search for neural networks
        q_res = self.client.post('/api/similarity/query', json={
            "query": "artificial neural networks and feature extraction",
            "top_k": 3
        })
        self.assertEqual(q_res.status_code, 200)
        q_data = q_res.get_json()
        self.assertGreater(q_data['total_matches'], 0)
        top_match = q_data['results'][0]
        self.assertEqual(top_match['text_id'], doc1_id)
        self.assertGreater(top_match['score'], 0.40)

        # Query search for baking
        q_bake = self.client.post('/api/similarity/query', json={
            "query": "fermenting sourdough with wild yeast",
            "top_k": 3
        })
        self.assertEqual(q_bake.status_code, 200)
        bake_data = q_bake.get_json()
        self.assertEqual(bake_data['results'][0]['text_id'], doc2_id)

        # Clean up
        del1 = self.client.delete(f'/api/texts/{doc1_id}')
        self.assertEqual(del1.status_code, 200)
        del2 = self.client.delete(f'/api/texts/{doc2_id}')
        self.assertEqual(del2.status_code, 200)

if __name__ == '__main__':
    unittest.main()
