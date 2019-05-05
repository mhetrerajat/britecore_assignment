import React, { PropTypes } from "react";
import uuidv1 from "uuid/v1";

const ChartController = ({
  distincts,
  startYear,
  endYear,
  onChangeEndYear,
  onChangeStartYear
}) => (
  <form className="form-inline">
    <div className="form-group">
      <label htmlFor="exampleFormControlSelect1">Start Year</label>
      <select
        className="custom-select my-1 mr-sm-2 ml-sm-1"
        id="startYear"
        defaultValue={startYear}
        onChange={onChangeStartYear}
      >
        {distincts.date_id.map((item, idx) => {
          return (
            <option key={uuidv1()} value={item}>
              {item}
            </option>
          );
        })}
      </select>
    </div>
    <div className="form-group">
      <label htmlFor="exampleFormControlSelect1">End Year</label>
      <select
        className="custom-select my-1 mr-sm-2 ml-sm-1"
        id="endYear"
        defaultValue={endYear}
        onChange={onChangeEndYear}
      >
        {distincts.date_id.map((item, idx) => {
          return (
            <option key={uuidv1()} value={item}>
              {item}
            </option>
          );
        })}
      </select>
    </div>
  </form>
);

export default ChartController;
