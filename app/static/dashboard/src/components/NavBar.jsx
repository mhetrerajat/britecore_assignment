import React from "react";

const NavBar = () => (
  <nav className="navbar navbar-expand-lg navbar-light bg-light">
    <div className="container">
      <a className="navbar-brand" href="#">
        Dashboard
      </a>
    </div>
    <div className="collapse navbar-collapse" id="navbarText">
      <span className="navbar-text">
        <a
          className="nav-link"
          href="https://github.com/mhetrerajat/britecore_assignment"
        >
          Github
        </a>
      </span>
    </div>
  </nav>
);

export default NavBar;
