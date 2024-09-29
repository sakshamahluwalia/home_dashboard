import express from 'express';
import cors from 'cors';
import billsRouter from './routes/bills';

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/bills', billsRouter);

// Default route
app.get('/', (req, res) => {
  res.send('Welcome to the bill tracker API!');
});

export default app;
