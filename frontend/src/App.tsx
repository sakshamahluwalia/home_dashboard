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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  ListItemText,
} from "@mui/material";
import { getBills, Bill, updateBill } from "./services/billsService";
import BillsTable from "./components/BillsTable";
import BillsChart from "./components/BillsChart";
import dayjs from "dayjs";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { darkTheme, lightTheme } from "./config/theme";

const App: React.FC = () => {
  const [bills, setBills] = useState<Bill[]>([]);
  const [chartType, setChartType] = useState<"line" | "bar">("bar");
  const [dataRange, setDataRange] = useState<"all" | "last4months">(
    "last4months"
  );
  const [filteredBills, setFilteredBills] = useState<Bill[]>([]);
  const [selectedProviders, setSelectedProviders] = useState<string[]>([]);
  const [uniqueProviders, setUniqueProviders] = useState<string[]>([]);

  // Theme state
  const [themeMode, setThemeMode] = useState<"light" | "dark">(() => {
    const savedTheme = localStorage.getItem("theme");
    return savedTheme === "dark" ? "dark" : "light";
  });

  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

  useEffect(() => {
    const fetchBills = async () => {
      try {
        const data = await getBills();
        setBills(data);
        const providers = Array.from(
          new Set(data.map((bill) => bill.service_provider))
        );
        setUniqueProviders(providers);
        setSelectedProviders(providers); // Default to all providers selected
      } catch (error) {
        console.error("Error fetching bills:", error);
      }
    };
    fetchBills();
  }, []);

  useEffect(() => {
    let filteredData = bills;

    // Filter by date range
    if (dataRange === "last4months") {
      const fourMonthsAgo = dayjs().subtract(4, "month");
      filteredData = filteredData.filter((bill) => {
        const billDate = dayjs(`${bill.year}-${bill.month}-01`);
        return billDate.isAfter(fourMonthsAgo);
      });
    }

    // Filter by selected service providers
    if (selectedProviders.length > 0) {
      filteredData = filteredData.filter((bill) =>
        selectedProviders.includes(bill.service_provider)
      );
    }

    setFilteredBills(filteredData);
  }, [bills, dataRange, selectedProviders]);

  useEffect(() => {
    localStorage.setItem("theme", themeMode);
  }, [themeMode]);

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

  const handleProviderChange = (
    event: React.ChangeEvent<{ value: unknown }>
  ) => {
    const value = event.target.value as string[];
    setSelectedProviders(value);
  };

  const handleThemeToggle = () => {
    setThemeMode(themeMode === "light" ? "dark" : "light");
  };

  const handleSaveEdit = async (updatedBill: Bill) => {
    try {
      const savedBill = await updateBill(updatedBill._id, updatedBill);
      // Update the bills state with the edited bill
      setBills(bills.map(bill => 
        bill._id === savedBill._id ? savedBill : bill
      ));
    } catch (error) {
      console.error('Failed to update bill:', error);
      // You might want to add error handling here (e.g., show a snackbar)
    }
  };

  // Sort bills for the table in descending order of date
  const sortedBills = [...filteredBills].sort((a, b) => {
    const dateA = dayjs(`${a.year}-${a.month}-01`);
    const dateB = dayjs(`${b.year}-${b.month}-01`);
    return dateB.valueOf() - dateA.valueOf();
  });

  return (
    <ThemeProvider theme={themeMode === "light" ? lightTheme : darkTheme}>
      <CssBaseline />
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
          sx={{ mb: 2, mx: 1 }}
        >
          {/* Chart Type Toggle */}
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

          {/* Data Range Toggle */}
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

          {/* Theme Toggle */}
          <ToggleButtonGroup
            color="primary"
            value={themeMode}
            exclusive
            onChange={handleThemeToggle}
          >
            <ToggleButton value="dark" sx={{ padding: "12px 16px" }}>
              Dark Mode
            </ToggleButton>
            <ToggleButton value="light" sx={{ padding: "12px 16px" }}>
              Light Mode
            </ToggleButton>
          </ToggleButtonGroup>

          {/* Service Provider Filter */}
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel id="service-provider-label">
              Service Provider
            </InputLabel>
            <Select
              labelId="service-provider-label"
              id="service-provider-select"
              multiple
              value={selectedProviders}
              // @ts-ignore
              onChange={handleProviderChange}
              renderValue={(selected) => (selected as string[]).join(", ")}
              label="Service Provider"
            >
              {uniqueProviders.map((provider) => (
                <MenuItem key={provider} value={provider}>
                  <Checkbox
                    checked={selectedProviders.indexOf(provider) > -1}
                  />
                  <ListItemText primary={provider} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Stack>

        <BillsChart bills={filteredBills} chartType={chartType} />
        <BillsTable 
          bills={sortedBills} 
          onSaveEdit={handleSaveEdit}
        />
      </Container>
    </ThemeProvider>
  );
};

export default App;
