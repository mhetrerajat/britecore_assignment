import React from "react";
import PropTypes from "prop-types";


const ErrorComponent = ({ message }) => (
  <div className="alert alert-danger" role="alert">
    {message}
. Please try again,
    {" "}
    <a className="alert-link" href="/">
      Retry
    </a>
  </div>
);

ErrorComponent.propTypes = {
  message: PropTypes.string
}

ErrorComponent.defaultProps = {
  message: ""
}

export default ErrorComponent;
