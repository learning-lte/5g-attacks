pragma solidity 0.8.4;

contract guard {

    address owner;
    bool attacked;
    mapping(address=>bool) public blackList;
    mapping(address=>uint256) public saltList;

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

    function _updateSalt(address user, uint256 salt) public onlyOwner validAddress(user) {
        saltList[user] = salt;
    }

    function updateSalts(address[] calldata users, uint256[] calldata salts) public {
        require(users.length == salts.length, "Input length is different");
        for (uint i = 0; i < users.length; i++) {
            _updateSalt(users[i], salts[i]);
        }
    }

    function _banUser(address addr) public onlyOwner validAddress(addr) {
        require(blackList[addr] != true, "Already Banned");
        blackList[addr] = true;
    }

    function banUsers(address[] calldata addrs) public {
        for (uint i = 0; i < addrs.length; i++) {
            _banUser(addrs[i]);
        }
    }

    function _recoverUser(address addr) public onlyOwner validAddress(addr) {
        require(blackList[addr] != false, "Already recovered");
        blackList[addr] = false;
    }

    function recoverUsers(address[] calldata addrs) public {
        for (uint i = 0; i < addrs.length; i++) {
            _recoverUser(addrs[i]);
        }
    }

    function _getSaltStatus(address addr) public view returns (uint256, bool) {
        uint256 salt = saltList[addr];
        bool status = blackList[addr];
        return (salt, status);
    }

    function getSaltStatuses(address[] calldata addrs) public view returns (uint256[] memory, bool[] memory) {
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