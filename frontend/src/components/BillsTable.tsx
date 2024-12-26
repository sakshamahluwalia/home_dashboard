import React, { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Tooltip,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import { Bill } from "../services/billsService";
import EditableRow from "./EditableRow";

interface BillsTableProps {
  bills: Bill[];
  onSaveEdit: (bill: Bill) => Promise<void>;
}

const BillsTable: React.FC<BillsTableProps> = ({ bills, onSaveEdit }) => {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState<Partial<Bill>>({});

  const handleEditClick = (bill: Bill) => {
    setEditingId(bill._id);
    setEditForm(bill);
  };

  const handleSave = async () => {
    if (editingId && editForm) {
      await onSaveEdit({ ...editForm, _id: editingId } as Bill);
      setEditingId(null);
    }
  };

  return (
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
                  xs: "none",
                  sm: "table-cell",
                },
              }}
            >
              Created At
            </TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {bills.map((bill) => (
            <TableRow key={bill._id}>
              {editingId === bill._id ? (
                <EditableRow
                  bill={bill}
                  editForm={editForm}
                  onSave={handleSave}
                  onCancel={() => setEditingId(null)}
                  onChange={(updates) => setEditForm({ ...editForm, ...updates })}
                />
              ) : (
                <>
                  <TableCell>{bill.service_provider}</TableCell>
                  <TableCell align="right">${bill.amount.toFixed(2)}</TableCell>
                  <TableCell align="right">{bill.month}</TableCell>
                  <TableCell align="right">{bill.year}</TableCell>
                  <TableCell
                    sx={{
                      display: {
                        xs: "none",
                        sm: "table-cell",
                      },
                    }}
                  >
                    {new Date(bill.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip title="Edit Bill">
                      <IconButton onClick={() => handleEditClick(bill)} size="small">
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default BillsTable; 