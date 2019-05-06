import axios from "axios";
import { keyBy, groupBy, forEach, round, uniq } from "lodash";

import API from "./api";

function cleanSummaryData(data) {
  const groupedByYear = groupBy(data, function(item) {
    return item.year;
  });
  const result = [];

  let productLines = [];

  let years = [];
  forEach(groupedByYear, function(value, year) {
    const groupedByProductLine = keyBy(value, "product_line");
    years.push(year);
    let item = {
      year
    };
    forEach(groupedByProductLine, function(premiumDetails, productLine) {
      item = Object.assign(item, {
        [productLine]: round(premiumDetails.earned_premium)
      });
      productLines.push(productLine);
    });

    result.push(item);
  });
  productLines = uniq(productLines);
  years = uniq(years);
  return { result, productLines, years };
}

const stateHandler = {
  setLoadingState(_this, loadingState) {
    _this.setState({ isLoading: loadingState });
  },
  setErrorState(_this, errorState, errorMessage) {
    _this.setState({
      isError: errorState,
      errorMessage
    });
  }
};

export function fetchInitState(_this, startYear, endYear) {
  stateHandler.setLoadingState(_this, true);
  axios
    .all([API.getReport(startYear, endYear), API.fetchDistinctValues()])
    .then(
      axios.spread(function(reportResponse, distinctResponse) {
        return {
          reportData: reportResponse.data.data,
          distinctData: distinctResponse.data.data
        };
      })
    )
    .then(function({ reportData, distinctData }) {
      const { result, productLines, years } = cleanSummaryData(reportData);
      _this.setState({
        data: result,
        productLines,
        years,
        startYear,
        endYear,
        distincts: distinctData
      });
    })
    .catch(function(err) {
      console.error(err);
      stateHandler.setErrorState(_this, true, err);
    })
    .finally(function() {
      stateHandler.setLoadingState(_this, false);
    });
}

export function getSummary(_this, startYear, endYear) {
  stateHandler.setLoadingState(_this, true);
  API.getReport(startYear, endYear)
    .then(response => {
      const { result, productLines, years } = cleanSummaryData(
        response.data.data
      );
      _this.setState({
        data: result,
        productLines,
        years,
        startYear,
        endYear
      });
    })
    .catch(function(error) {
      console.log(error);
      stateHandler.setErrorState(_this, true, error);
    })
    .finally(function() {
      stateHandler.setLoadingState(_this, false);
    });
}
