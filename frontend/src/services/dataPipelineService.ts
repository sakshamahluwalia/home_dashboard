import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';

/**
 * Triggers data extraction by calling the backend's endpoint.
 * @protected Requires API key or proper authentication.
 */
export const triggerDataExtraction = async (): Promise<void> => {
  try {
    await axios.get(`${API_URL}/data-pipeline`);
  } catch (error) {
    console.error('Error triggering data extraction:', error);
    throw error;
  }
}; 