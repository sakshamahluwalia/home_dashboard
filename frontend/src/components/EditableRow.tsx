import React from 'react';
import {
  TableCell,
  TextField,
  IconButton,
  Tooltip,
} from "@mui/material";
import SaveIcon from "@mui/icons-material/Save";
import CancelIcon from "@mui/icons-material/Cancel";
import { Bill } from "../services/billsService";

interface EditableRowProps {
  bill: Bill;
  editForm: Partial<Bill>;
  onSave: () => Promise<void>;
  onDelete: () => Promise<void>;
  onChange: (updates: Partial<Bill>) => void;
}

const EditableRow: React.FC<EditableRowProps> = ({
  bill,
  editForm,
  onSave,
  onDelete,
  onChange,
}) => {
  return (
    <>
      <TableCell>
        <TextField
          fullWidth
          value={editForm.service_provider || ''}
          onChange={(e) => onChange({ service_provider: e.target.value })}
        
        />
      </TableCell>
      <TableCell align="right">
        <TextField
          type="number"
          value={editForm.amount || ''}
          onChange={(e) => onChange({ amount: parseFloat(e.target.value) })}
        
        />
      </TableCell>
      <TableCell align="right">
        <TextField
          type="number"
          value={editForm.month || ''}
          onChange={(e) => onChange({ month: parseInt(e.target.value) })}
        
          inputProps={{ min: 1, max: 12 }}
        />
      </TableCell>
      <TableCell align="right">
        <TextField
          type="number"
          value={editForm.year || ''}
          onChange={(e) => onChange({ year: parseInt(e.target.value) })}
        
        />
      </TableCell>
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
        <Tooltip title="Save">
          <IconButton onClick={onSave} color="primary">
            <SaveIcon />
          </IconButton>
        </Tooltip>
        <Tooltip title="Delete">
          <IconButton onClick={onDelete} color="error">
            <CancelIcon />
          </IconButton>
        </Tooltip>
      </TableCell>
    </>
  );
};

export default EditableRow; 