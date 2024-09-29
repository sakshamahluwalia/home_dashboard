// src/App.tsx
import React, { useEffect, useState } from "react";
import {
  Container,
  Typography,
  ToggleButton,
  ToggleButtonGroup,
  Stack,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import { getBills, Bill } from "./services/billsService";
import BillsTable from "./components/BillsTable";
import BillsChart from "./components/BillsChart";
import dayjs from "dayjs";

const App: React.FC = () => {
  const [bills, setBills] = useState<Bill[]>([]);
  const [chartType, setChartType] = useState<"line" | "bar">("bar");
  const [dataRange, setDataRange] = useState<"all" | "last4months">(
    "last4months"
  );
  const [filteredBills, setFilteredBills] = useState<Bill[]>([]);

  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

  useEffect(() => {
    const fetchBills = async () => {
      try {
        const data = await getBills();
        setBills(data);
      } catch (error) {
        console.error("Error fetching bills:", error);
      }
    };
    fetchBills();
  }, []);

  useEffect(() => {
    let filteredData = bills;

    if (dataRange === "last4months") {
      const sixMonthsAgo = dayjs().subtract(4, "month");
      filteredData = bills.filter((bill) => {
        const billDate = dayjs(bill.year + "-" + bill.month);
        return billDate.month() >= sixMonthsAgo.month();
      });
    }

    setFilteredBills(filteredData);
  }, [bills, dataRange]);

  const handleChartTypeChange = (
    event: React.MouseEvent<HTMLElement>,
    newChartType: "line" | "bar" | null
  ) => {
    if (newChartType !== null) {
      setChartType(newChartType);
    }
  };

  const handleDataRangeChange = (
    event: React.MouseEvent<HTMLElement>,
    newRange: "all" | "last4months" | null
  ) => {
    if (newRange !== null) {
      setDataRange(newRange);
    }
  };

  // Optionally sort bills for the table
  const sortedBills = [...filteredBills].sort((a, b) => {
    const dateA = new Date(a.year, a.month - 1);
    const dateB = new Date(b.year, b.month - 1);
    return dateB.getTime() - dateA.getTime();
  });

  return (
    <Container
      sx={{
        px: [0, 2],
      }}
    >
      <Typography
        variant={isSmallScreen ? "h5" : "h4"}
        align="center"
        gutterBottom
        sx={{ marginTop: 4 }}
      >
        Bills Dashboard
      </Typography>

      <Stack
        direction={isSmallScreen ? "column" : "row"}
        spacing={2}
        sx={{ marginBottom: 2 }}
      >
        <ToggleButtonGroup
          color="primary"
          value={chartType}
          exclusive
          onChange={handleChartTypeChange}
        >
          <ToggleButton value="bar" sx={{ padding: "12px 16px" }}>
            Stacked Bar Chart
          </ToggleButton>
          <ToggleButton value="line" sx={{ padding: "12px 16px" }}>
            Line Chart
          </ToggleButton>
        </ToggleButtonGroup>

        <ToggleButtonGroup
          color="primary"
          value={dataRange}
          exclusive
          onChange={handleDataRangeChange}
        >
          <ToggleButton value="last4months" sx={{ padding: "12px 16px" }}>
            Last 4 Months
          </ToggleButton>
          <ToggleButton value="all" sx={{ padding: "12px 16px" }}>
            All Data
          </ToggleButton>
        </ToggleButtonGroup>
      </Stack>

      <BillsChart bills={filteredBills} chartType={chartType} />
      <BillsTable bills={sortedBills} />
    </Container>
  );
};

export default App;
