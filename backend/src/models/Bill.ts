import { Schema, model, Document } from 'mongoose';

export interface IBill extends Document {
  service_provider: string;
  amount: number;
  month: number;
  year: number;
  created_at?: Date;
  updated_at?: Date;
}

const BillSchema = new Schema<IBill>(
  {
    service_provider: { type: String, required: true },
    amount: { type: Number, required: true },
    month: { type: Number, required: true, min: 1, max: 12 },
    year: { type: Number, required: true },
    created_at: { type: Date, default: Date.now },
    updated_at: { type: Date },
  },
  {
    collection: 'bills',
    versionKey: false,
  }
);

// Create a unique index on service_provider, year, and month
BillSchema.index({ service_provider: 1, year: 1, month: 1 }, { unique: true });

export const Bill = model<IBill>('Bill', BillSchema);
