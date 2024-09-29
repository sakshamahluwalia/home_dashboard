// src/components/BillsTable.tsx
import React from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import { Bill } from "../services/billsService";

interface BillsTableProps {
  bills: Bill[];
}

const BillsTable: React.FC<BillsTableProps> = ({ bills }) => (
  <TableContainer component={Paper} sx={{ marginTop: 4 }}>
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Service Provider</TableCell>
          <TableCell align="right">Amount</TableCell>
          <TableCell align="right">Month</TableCell>
          <TableCell align="right">Year</TableCell>
          <TableCell
            sx={{
              display: {
                xs: "none", // hide on extra-small screens
                sm: "table-cell", // show on small screens and up
              },
            }}
          >
            Created At
          </TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {bills.map((bill) => (
          <TableRow key={bill._id}>
            <TableCell>{bill.service_provider}</TableCell>
            <TableCell align="right">${bill.amount.toFixed(2)}</TableCell>
            <TableCell align="right">{bill.month}</TableCell>
            <TableCell align="right">{bill.year}</TableCell>
            <TableCell
              sx={{
                display: {
                  xs: "none", // hide on extra-small screens
                  sm: "table-cell", // show on small screens and up
                },
              }}
            >
              {new Date(bill.created_at).toLocaleDateString()}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);

export default BillsTable;
