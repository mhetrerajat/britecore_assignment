import React from "react";

import { gt } from "lodash";
import SummaryChart from "../components/SummaryChart";
import LoadingComponent from "../components/LoadingComponent";
import ErrorComponent from "../components/ErrorComponent";
import NavBar from "../components/NavBar";

import { getSummary, fetchInitState } from "../utils";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      productLines: [],
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

    this.onChangeEndYear = this.onChangeEndYear.bind(this);
    this.onChangeStartYear = this.onChangeStartYear.bind(this);
  }

  componentDidMount() {
    const { startYear, endYear } = this.state;
    fetchInitState(this, startYear, endYear);
  }

  onChangeStartYear(event) {
    const startYear = event.target.value;
    const { endYear } = this.state;
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
    const endYear = event.target.value;
    const { startYear } = this.state;
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
    const {
      data,
      productLines,
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
          productLines={productLines}
          distincts={distincts}
          startYear={startYear}
          endYear={endYear}
          onChangeEndYear={this.onChangeEndYear}
          onChangeStartYear={this.onChangeStartYear}
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
