function bug(){
        require(not_called);
        if( ! (msg.sender.call() ) ){
            throw;
        }
        not_called = False;
    } 