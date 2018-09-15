import React, { Component } from "react";
import { BrowserRouter, Route, Redirect, Switch } from "react-router-dom";
import Home from "./components/Home";

const App = () => (
  <BrowserRouter>
    <Switch>
      <Route exact path="/" render={() => <Home />} />
    </Switch>
  </BrowserRouter>
);

export default App;
