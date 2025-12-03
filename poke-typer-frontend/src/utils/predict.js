import axios from "axios";

const API_BASE = "http://localhost:10000";

/**
 * Upload an image and get predictions from the Flask backend.
 * @param {File} file - The image file to upload.
 * @param {string} model - The model name (A, B, C, D, E).
 * @returns {Promise<Object>} The parsed JSON response from the backend.
 */
export async function predictType(file, model = "A") {
  if (!file) throw new Error("No file provided");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${API_BASE}/predict/${model}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data; // { model: 'A', prediction: {...} }
  } catch (error) {
    console.error("Prediction request failed:", error);
    throw new Error(
      error.response?.data?.error || "Failed to get prediction from server."
    );
  }
}
