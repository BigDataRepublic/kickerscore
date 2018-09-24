import React from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import Home from "./components/Home";
import AddPlayer from "./components/AddPlayer";
import AddMatch from "./components/AddMatch";

const App = () => (
  <BrowserRouter>
    <Switch>
      <Route exact path="/" render={() => <Home />} />
      <Route exact path="/add-player" render={() => <AddPlayer />} />
      <Route exact path="/add-match" render={() => <AddMatch />} />
    </Switch>
  </BrowserRouter>
);

export default App;
