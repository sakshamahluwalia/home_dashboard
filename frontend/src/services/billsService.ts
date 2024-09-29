// src/services/billsService.ts
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';

export interface Bill {
  _id: string;
  service_provider: string;
  amount: number;
  month: number;
  year: number;
  created_at: string;
}

export const getBills = async (): Promise<Bill[]> => {
  try {
    const response = await axios.get<Bill[]>(`${API_URL}/bills`);
    return response.data;
  } catch (error) {
    console.error('Error fetching bills data:', error);
    throw error;
  }
};
