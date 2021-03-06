import React from "react";
import {BrowserRouter, Route, Switch} from "react-router-dom";
import Home from "./components/Home";
import AddMatch from "./components/AddMatch";
import AddPhotoMatch from "./components/AddPhotoMatch";
import Navbar from "./components/Navigation";

const App = () => (
    <BrowserRouter>
        <div>
            <Navbar/>
            <Switch>
                <Route exact path="/" render={() => <Home/>}/>
                <Route exact path="/add-photo-match" render={() => <AddPhotoMatch/>}/>
                <Route exact path="/add-match" render={() => <AddMatch/>}/>
            </Switch>
        </div>
    </BrowserRouter>
);

export default App;
