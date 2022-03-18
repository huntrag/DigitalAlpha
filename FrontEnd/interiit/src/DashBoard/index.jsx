import * as React from "react";
import {useLocation} from "react-router-dom";
import {Button, Card, Collapse, Grid, TextField} from "@mui/material";
import LocalizationProvider from "@mui/lab/LocalizationProvider";
import DatePicker from "@mui/lab/DatePicker";
import Appbar from "../AppBar/index";
import DetailList from "./ListDetail";
import ComplexData from "./Table";
import DateAdapter from "@mui/lab/AdapterDateFns";
import Moment from "react-moment";
import GraphCard from "./DashBoard1";
import "moment-timezone";
import axios from "axios";
export default function DashBoard() {
  const [GraphData, setGraphData] = React.useState(null)
  const {state} = useLocation();
  const {data} = state;
  const [expanded, setExpanded] = React.useState(false);
  const [value, setValue] = React.useState(Date());
  const [expandedForChart, setExpanedForChart] = React.useState(false);
  const [FinalExpandedForCharts, setFinalExpandedForCharts] =
    React.useState(false);
  // console.log(data, "hue");
  function convert(str) {
    var date = new Date(str),
      mnth = ("0" + (date.getMonth() + 1)).slice(-2),
      day = ("0" + date.getDate()).slice(-2);
    return [date.getFullYear(), mnth, day].join("-");
  }

  //  {
  //        "date":"2017-01-01",
  //        "cik":796343
  //    }

  async function showAllGraphs() {
    setFinalExpandedForCharts(!FinalExpandedForCharts)
    let date = convert(value.toString());
    setValue(date);
    const sendObj = {
      date: date,
      cik: data.cik,
    };
    let params = JSON.stringify(sendObj);
    // console.log(JSON.stringify(sendObj));
    // console.log(typeof date, data.cik);
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/bs?q1=${sendObj.cik}&q2=${date}`
      );
      console.log(response.data,"res");
      setGraphData(response.data);

    } catch (error) {
      console.log(error);
    }
  }
  return (
    <>
      <LocalizationProvider dateAdapter={DateAdapter}>
        <Appbar />
        <Grid
          container
          spacing={0}
          direction="column"
          alignItems="center"
          justifyContent="center"
        >
          <Grid item xs={3}>
            <Grid
              container
              spacing={10}
              alignItems="center"
              columnSpacing={1}
              justifyContent="center"
            >
              <Grid item xs={12} sm={12} md={6}>
                <Card sx={{maxWidth: 645}}>
                  <DetailList data={data} />
                  <Button
                    onClick={() => {
                      setExpanded(!expanded);
                    }}
                  >
                    {!expanded
                      ? `See More Details About Company`
                      : `See Less Details About Company`}
                  </Button>
                  <Collapse in={expanded} timeout="auto" unmountOnExit>
                    <ComplexData data={data} />
                  </Collapse>
                  <Button
                    onClick={() => {
                      setExpanedForChart(!expandedForChart);
                    }}
                  >
                    {!expandedForChart ? `See charts` : `Unsee Charts`}
                  </Button>
                  <Collapse in={expandedForChart} timeout="auto" unmountOnExit>
                    <Grid
                      container
                      spacing={0}
                      direction="column"
                      alignItems="center"
                      justifyContent="center"
                    >
                      <Grid item xs={3}>
                        <DatePicker
                          disableFuture
                          label="Enter The Date For Viewing Graphs"
                          openTo="year"
                          views={["year", "month", "day"]}
                          value={value}
                          onChange={(newValue) => {
                            setValue(newValue);
                          }}
                          renderInput={(params) => (
                            <TextField
                              {...params}
                              style={{
                                marginBottom: "12px",
                                marginTop: "22px",
                              }}
                            />
                          )}
                        />
                      </Grid>

                      <Grid item xs={3}>
                        <Button
                          style={{marginBottom: "22px"}}
                          onClick={showAllGraphs}
                        >
                          {!FinalExpandedForCharts ? `See Graphs` : `Unsee Graphs`}
                        </Button>
                        <Collapse in={FinalExpandedForCharts} style={{width: "800px"}} timeout="auto" unmountOnExit>
                          <GraphCard data={GraphData} />
                        </Collapse>
                      </Grid>
                    </Grid>
                  </Collapse>
                </Card>
              </Grid>
              <Grid item xs={12} sm={12} md={6}>
                <Card sx={{maxWidth: 645}}>
                  <DetailList data={data} />
                  <Button
                    onClick={() => {
                      setExpanedForChart(!expandedForChart);
                    }}
                  >
                    {!expandedForChart
                      ? `See More Details`
                      : `See Less Details`}
                  </Button>
                </Card>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </LocalizationProvider>
    </>
  );
}
