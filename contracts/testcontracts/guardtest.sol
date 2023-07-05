pragma solidity 0.8.4;

contract guard {

    address owner;
    bool attacked;
    mapping(uint256=>bool) public blackList;
    mapping(uint256=>uint256) public saltList;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier validAddress(address _addr) {
        require(_addr != address(0), "Not valid address");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function getUDMStatus() public view returns(bool) {
        return attacked;
    }

    function changeOwner(address _newOwner) public onlyOwner validAddress(_newOwner) {
        owner = _newOwner;
    }

    function changeUDMStatus() public onlyOwner {
        attacked = !attacked;
    }

    function _updateSalt(uint256 user, uint256 salt) public onlyOwner {
        saltList[user] = salt;
    }

    function updateSalts(uint256[] calldata users, uint256[] calldata salts) public {
        require(users.length == salts.length, "Input length is different");
        for (uint i = 0; i < users.length; i++) {
            _updateSalt(users[i], salts[i]);
        }
    }

    function _banUser(uint256 addr) public onlyOwner {
        require(blackList[addr] != true, "Already Banned");
        blackList[addr] = true;
    }

    function banUsers(uint256[] calldata addrs) public {
        for (uint i = 0; i < addrs.length; i++) {
            _banUser(addrs[i]);
        }
    }

    function _recoverUser(uint256 addr) public onlyOwner {
        require(blackList[addr] != false, "Already recovered");
        blackList[addr] = false;
    }

    function recoverUsers(uint256[] calldata addrs) public {
        for (uint i = 0; i < addrs.length; i++) {
            _recoverUser(addrs[i]);
        }
    }

    function _getSaltStatus(uint256 addr) public view returns (uint256, bool) {
        uint256 salt = saltList[addr];
        bool status = blackList[addr];
        return (salt, status);
    }

    function getSaltStatuses(uint256[] calldata addrs) public view returns (uint256[] memory, bool[] memory) {
        uint256[] memory salts = new uint256[](addrs.length);
        bool[] memory status = new bool[](addrs.length);
        for (uint i = 0; i < addrs.length; i++) {
            (uint256 salt, bool stat) = _getSaltStatus(addrs[i]);
            salts[i] = salt;
            status[i] = stat;
        }
        return (salts, status);
    }
}
