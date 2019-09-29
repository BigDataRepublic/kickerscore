import React from 'react';
import {
  Navbar,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  Media} from 'reactstrap';
import BDRLogo from "./Logo-Elephant.png";

let imgStyle = {
  maxHeight: '64px',
  maxWidth: '64px'
};

let navFontStyle = {
  fontSize: '37px',
  margin: '0 0 0 100px'
};

export default class Navigation extends React.Component {
  constructor(props) {
    super(props);

    this.toggle = this.toggle.bind(this);
    this.state = {
      isOpen: false
    };
  }
  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }
  render() {
    return (
      <div>
        <Navbar color="light" light expand="md">
          <NavbarBrand href="/">
            <Media left>
              <Media object style={imgStyle} src={ BDRLogo } alt="My PlaceHolder Picture" />
            </Media>
          </NavbarBrand>
            <Nav className="ml-auto" navbar>
          <NavItem>
            <NavLink href="/"><div style={navFontStyle}>Leaderboard</div></NavLink>
          </NavItem>
          <NavItem>
            <NavLink href="/add-photo-match/"><div style={navFontStyle}>Add Match</div></NavLink>
          </NavItem>
            </Nav>
        </Navbar>
      </div>
    );
  }
}
