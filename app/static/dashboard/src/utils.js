import axios from "axios";
import { keyBy, groupBy, forEach, round, uniq, gt } from "lodash";

import API from "./api";

function cleanSummaryData(data) {
  let groupedByYear = groupBy(data, function(item) {
    return item.year;
  });
  let result = [],
    productLines = [],
    years = [];
  forEach(groupedByYear, function(value, year) {
    let groupedByProductLine = keyBy(value, "product_line");
    years.push(year);
    let item = {
      year: year
    };
    forEach(groupedByProductLine, function(premiumDetails, productLine) {
      item = Object.assign(item, {
        [productLine]: round(premiumDetails["earned_premium"])
      });
      productLines.push(productLine);
    });

    result.push(item);
  });
  productLines = uniq(productLines);
  years = uniq(years);
  return { result, productLines, years };
}

let stateHandler = {
  setLoadingState: function(_this, loadingState) {
    _this.setState({ isLoading: loadingState });
  },
  setErrorState: function(_this, errorState, errorMessage) {
    _this.setState({
      isError: errorState,
      errorMessage: errorMessage
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
      let { result, productLines, years } = cleanSummaryData(reportData);
      _this.setState({
        data: result,
        product_lines: productLines,
        years: years,
        startYear: startYear,
        endYear: endYear,
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
      let { result, productLines, years } = cleanSummaryData(
        response.data.data
      );
      _this.setState({
        data: result,
        product_lines: productLines,
        years: years,
        startYear: startYear,
        endYear: endYear
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
