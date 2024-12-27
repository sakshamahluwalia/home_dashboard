import { Router, Request, Response } from 'express';
import axios from 'axios';

const router = Router();

// Data Pipeline API URL
const DATA_PIPELINE_URL = process.env.DATA_PIPELINE_URL || 'http://localhost:3001/';

/**
 * @route   POST /api/data-pipeline/trigger-extraction
 * @desc    Trigger data extraction in the data-pipeline service
 * @access  Protected
 */
router.get('/', async (req: Request, res: Response) => {
  try {
    // Send a POST request to the data-pipeline's Flask API to trigger extraction
    const response = await axios.get(`${DATA_PIPELINE_URL}/start`, {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 10000, // Optional: Set a timeout for the request
    });

    console.log(response.data);

    if (response.status === 200) {
      res.status(200).json({ message: 'Data extraction initiated successfully.' });
    } else {
      res.status(response.status).json({ message: 'Failed to initiate data extraction.', details: response.data });
    }
  } catch (error: any) {
    console.error('Error triggering data extraction:', error.message);
    res.status(500).json({ message: 'Internal Server Error: Could not trigger data extraction.', error: error.message });
  }
});

export default router; 