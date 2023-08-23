contract ReentrantContract {
	function f() external {
		if (BugReentrancyEvents(msg.sender).counter() == 1) {
			BugReentrancyEvents(msg.sender).count(this);
		}
	}
}
contract Counter {
	uint public counter;
	event Counter(uint);

}
contract BugReentrancyEvents is Counter {
    function count(ReentrantContract d) external {
        counter += 1;
        d.f();
        emit Counter(counter);
    }
}
contract NoReentrancyEvents is Counter {
	function count(ReentrantContract d) external {
        counter += 1;
        emit Counter(counter);
        d.f();
    }
}