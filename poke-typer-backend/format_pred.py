import numpy as np

TYPE_INDEX = [
    'bug','dark','dragon','electric','fairy','fighting','fire','flying',
    'ghost','grass','ground','ice','normal','poison','psychic','rock','steel','water'
]

def format_prediction(pred_array):
    probs = np.squeeze(pred_array)
    return {
        TYPE_INDEX[i]: round(float(prob), 4)
        for i, prob in enumerate(probs)
    }
