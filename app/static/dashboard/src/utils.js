import axios from "axios";
import { keyBy, groupBy, forEach, round, uniq, gt } from "lodash";

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

export function getSummary(_this, startYear, endYear) {
  const apiURL =
    "/api/v1/report/?group_by=year&group_by=product_line&start_year=" +
    startYear +
    "&end_year=" +
    endYear;
  _this.setState({ isLoading: true });
  axios
    .get(apiURL)
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
      _this.setState({
        isError: true,
        errorMessage: error
      });
    })
    .finally(function() {
      _this.setState({
        isLoading: false
      });
    });
}

export function fetchDistinctValues(_this) {
  const apiURL = "/api/v1/distinct";
  axios
    .get(apiURL)
    .then(response => {
      _this.setState({
        distincts: response.data.data
      });
    })
    .catch(function(error) {
      console.log(error);
      _this.setState({
        isError: true,
        errorMessage: error
      });
    });
}
