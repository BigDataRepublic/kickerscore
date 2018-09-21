import React, { Component } from "react";
import { BrowserRouter, Route, Redirect, Switch } from "react-router-dom";
import Home from "./components/Home";
import AddPlayer from "./components/AddPlayer";

const App = () => (
  <BrowserRouter>
    <Switch>
      <Route exact path="/" render={() => <Home />} />
      <Route exact path="/add-player" render={() => <AddPlayer />} />
    </Switch>
  </BrowserRouter>
);

export default App;
