// This component handles the App template used on every page.
import React from 'react';
import PropTypes from 'prop-types';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { connect } from 'react-redux';
import Manual from './Manual';
import Login from './auth/Login';
import PrivateRoute from './auth/PrivateRoute';

const App = ({ authenticated, checked }) => (
  <Router>
    { checked &&
      <div>
        <PrivateRoute exact path="/" component={Manual} authenticated={authenticated}/>
        <Route path="/login" component={Login}/>
      </div>
    }
  </Router>
);

const { bool } = PropTypes;

App.propTypes = {
  authenticated: bool.isRequired,
  checked: bool.isRequired
};

const mapState = ({ session }) => ({
  checked: session.checked,
  authenticated: session.authenticated
});

export default connect(mapState)(App);
