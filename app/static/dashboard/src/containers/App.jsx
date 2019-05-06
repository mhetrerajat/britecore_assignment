import React, { PropTypes } from "react";

import SummaryChart from "../components/SummaryChart";
import LoadingComponent from "../components/LoadingComponent";
import ErrorComponent from "../components/ErrorComponent";
import NavBar from "../components/NavBar";

import { getSummary, fetchDistinctValues, fetchInitState } from "../utils";

import { gt } from "lodash";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      product_lines: [],
      years: [],
      data: [],
      distincts: {
        date_id: [],
        agency_id: [],
        line: []
      },
      startYear: "2005",
      endYear: "2007",
      isLoading: false,
      isError: false,
      errorMessage: ""
    };
  }

  componentWillMount() {
    //fetchDistinctValues(this);
  }

  componentDidMount() {
    let { startYear, endYear } = this.state;
    //getSummary(this, startYear, endYear);
    fetchInitState(this, startYear, endYear);
  }

  onChangeStartYear(event) {
    let startYear = event.target.value;
    let { endYear } = this.state;
    if (gt(endYear, startYear)) {
      getSummary(this, startYear, endYear);
    } else {
      this.setState({
        isError: true,
        errorMessage: "Start year cannot be greater than end year"
      });
    }
  }

  onChangeEndYear(event) {
    let endYear = event.target.value;
    let { startYear } = this.state;
    if (gt(endYear, startYear)) {
      getSummary(this, startYear, endYear);
    } else {
      this.setState({
        isError: true,
        errorMessage: "Start year cannot be greater than end year"
      });
    }
  }

  render() {
    let {
      data,
      product_lines,
      years,
      distincts,
      startYear,
      endYear,
      isLoading,
      isError,
      errorMessage
    } = this.state;

    let premiumEarnedComponent = <LoadingComponent />;
    if (!isLoading && !isError) {
      premiumEarnedComponent = (
        <SummaryChart
          data={data}
          product_lines={product_lines}
          years={years}
          distincts={distincts}
          startYear={startYear}
          endYear={endYear}
          onChangeEndYear={this.onChangeEndYear.bind(this)}
          onChangeStartYear={this.onChangeStartYear.bind(this)}
        />
      );
    } else if (isError) {
      premiumEarnedComponent = <ErrorComponent message={errorMessage} />;
    }

    return (
      <div className="container">
        <NavBar />
        <div className="row mt-3">
          <div className="col">{premiumEarnedComponent}</div>
        </div>
      </div>
    );
  }
}

export default App;
