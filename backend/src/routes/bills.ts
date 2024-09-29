import { Router, Request, Response } from 'express';
import { Bill, IBill } from '../models/Bill';

const router = Router();

// Create a new bill
router.post('/', async (req: Request, res: Response) => {
  try {
    const billData: IBill = req.body;
    const bill = new Bill(billData);
    const savedBill = await bill.save();
    res.status(201).json(savedBill);
  } catch (error: any) {
    if (error.code === 11000) {
      // Duplicate key error
      return res.status(400).json({ message: 'Bill already exists for this service provider, year, and month.' });
    }
    res.status(500).json({ message: 'Server error', error });
  }
});

// Get all bills or filter by query parameters
router.get('/', async (req: Request, res: Response) => {
  try {
    const { service_provider, year, month } = req.query;

    const query: any = {};

    if (service_provider) query.service_provider = service_provider;
    if (year) query.year = parseInt(year as string);
    if (month) query.month = parseInt(month as string);

    const bills = await Bill.find(query);
    res.json(bills);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
});

// Get a bill by ID
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const bill = await Bill.findById(req.params.id);
    if (!bill) return res.status(404).json({ message: 'Bill not found' });
    res.json(bill);
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
});

// Update a bill by ID
router.put('/:id', async (req: Request, res: Response) => {
  try {
    const updatedBill = await Bill.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!updatedBill) return res.status(404).json({ message: 'Bill not found' });
    res.json(updatedBill);
  } catch (error: any) {
    if (error.code === 11000) {
      // Duplicate key error
      return res.status(400).json({ message: 'Another bill exists with the same service provider, year, and month.' });
    }
    res.status(500).json({ message: 'Server error', error });
  }
});

// Delete a bill by ID
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const deletedBill = await Bill.findByIdAndDelete(req.params.id);
    if (!deletedBill) return res.status(404).json({ message: 'Bill not found' });
    res.json({ message: 'Bill deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Server error', error });
  }
});

export default router;
