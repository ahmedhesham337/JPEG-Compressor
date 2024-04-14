'use client';

import Navbar from 'react-bootstrap/Navbar';
import Link from "next/link";

export default function NavBar(){
    return(
        <>
        <Navbar variant="dark" bg="dark" expand="lg" className="p-2">
          <Navbar.Brand as={Link} href="/">JPEG Compressor</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
          </Navbar.Collapse>
        </Navbar>
      </>
    );
}
