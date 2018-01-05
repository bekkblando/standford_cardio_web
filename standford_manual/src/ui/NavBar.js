import React, { Component } from 'react';


class NavBar extends Component {
  render () {
    return(
      <nav>
        <div id="nav-wrapper">
          <ul id="nav-mobile" className="left hide-on-med-and-down">
            <a className="brand-logo right">Cardio</a>
            { this.props.auth &&
              <span>
                <li><a href="/manual">Manual</a></li>
                <li><a href="/logout">Logout</a></li>
              </span>
            }
            { !this.props.auth &&
              <li><a href="/login">Login</a></li>
            }
          </ul>
        </div>
      </nav>
  );
  }
}

export default NavBar;
