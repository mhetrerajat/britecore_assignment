import React from "react";

const ErrorComponent = ({ message }) => (
  <div className="alert alert-danger" role="alert">
    {message}. Please try again,{" "}
    <a className="alert-link" href="/">
      Retry
    </a>
  </div>
);

export default ErrorComponent;
