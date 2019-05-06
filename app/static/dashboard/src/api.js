import axios from "axios";

const API = {
  getReport(startYear, endYear) {
    const apiURL =
      `/api/v1/report/?group_by=year&group_by=product_line&start_year=${ 
      startYear 
      }&end_year=${ 
      endYear}`;
    return axios.get(apiURL);
  },
  fetchDistinctValues() {
    const apiURL = "/api/v1/distinct";
    return axios.get(apiURL);
  }
};

export default API;
