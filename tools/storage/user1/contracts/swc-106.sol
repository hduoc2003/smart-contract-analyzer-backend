pragma solidity 0.4.11;

contract SimpleSuicide {

  function sudicideAnyone() {
    selfdestruct(msg.sender);
  }

}
