/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable jsx-a11y/label-has-associated-control */
import React from "react";
import uuidv1 from "uuid/v1";
import PropTypes from "prop-types";

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
        {distincts.date_id.map(item => {
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
        {distincts.date_id.map((item) => {
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

ChartController.propTypes = {
  distincts: PropTypes.instanceOf(Object),
  endYear: PropTypes.string,
  onChangeEndYear: PropTypes.func,
  onChangeStartYear: PropTypes.func,
  startYear: PropTypes.string
};

ChartController.defaultProps = {
  distincts: { date_id: [], agency_id: [], line: [] },
  endYear: "2007",
  startYear: "2005",
  onChangeEndYear: () => {},
  onChangeStartYear: () => {}
};

export default ChartController;
