import React, { useState } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Redirect,
  Switch
} from 'react-router-dom'

// import logo from './logo.svg';
import './stylesheets/App.css';
import Home from './components/Home';
import AddQuestionView from './components/AddQuestionView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';
import Login from './components/Login';
import { useAppContext } from "./libs/contextLib";


function App() {

    const { isAuthenticated } = useAppContext();

    // A wrapper for <Route> that redirects to the login screen if you're not yet authenticated.
    // https://stackoverflow.com/a/45768790
    // https://reactrouter.com/web/example/auth-workflow
    function PrivateRoute({ children, ...rest }) {
      return (
        <Route
          {...rest}
          render={({ location }) =>
            isAuthenticated ? (
              children
            ) : (
              <Redirect
                to={{
                  pathname: "/login",
                  state: { from: location }
                }}
              />
            )
          }
        />
      );
    }

    return (
        <div className="App">
          <Router>
            <Header path />
            <Switch>
              <PrivateRoute path="/list" exact>
                <QuestionView />
              </PrivateRoute>
              <PrivateRoute path="/add">
                <AddQuestionView />
              </PrivateRoute>
              <PrivateRoute path="/play">
                <QuizView />
              </PrivateRoute>
              <Route path="/login">
                <Login />
              </Route>
              <Route path="/">
                <Home />
              </Route>
            </Switch>
          </Router>
        </div>
    );
}

export default App;
