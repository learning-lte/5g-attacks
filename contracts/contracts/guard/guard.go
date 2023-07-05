// Code generated - DO NOT EDIT.
// This file is a generated binding and any manual changes will be lost.

package guard

import (
	"errors"
	"math/big"
	"strings"

	ethereum "github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/accounts/abi"
	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/event"
)

// Reference imports to suppress errors if they are not otherwise used.
var (
	_ = errors.New
	_ = big.NewInt
	_ = strings.NewReader
	_ = ethereum.NotFound
	_ = bind.Bind
	_ = common.Big1
	_ = types.BloomLookup
	_ = event.NewSubscription
	_ = abi.ConvertType
)

// GuardMetaData contains all meta data concerning the Guard contract.
var GuardMetaData = &bind.MetaData{
	ABI: "[{\"inputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"addr\",\"type\":\"address\"}],\"name\":\"_banUser\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"addr\",\"type\":\"address\"}],\"name\":\"_getSaltStatus\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"},{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"addr\",\"type\":\"address\"}],\"name\":\"_recoverUser\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"user\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"salt\",\"type\":\"uint256\"}],\"name\":\"_updateSalt\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address[]\",\"name\":\"addrs\",\"type\":\"address[]\"}],\"name\":\"banUsers\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"name\":\"blackList\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"_newOwner\",\"type\":\"address\"}],\"name\":\"changeOwner\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"changeUDMStatus\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address[]\",\"name\":\"addrs\",\"type\":\"address[]\"}],\"name\":\"getSaltStatuses\",\"outputs\":[{\"internalType\":\"uint256[]\",\"name\":\"\",\"type\":\"uint256[]\"},{\"internalType\":\"bool[]\",\"name\":\"\",\"type\":\"bool[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getUDMStatus\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address[]\",\"name\":\"addrs\",\"type\":\"address[]\"}],\"name\":\"recoverUsers\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"name\":\"saltList\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address[]\",\"name\":\"users\",\"type\":\"address[]\"},{\"internalType\":\"uint256[]\",\"name\":\"salts\",\"type\":\"uint256[]\"}],\"name\":\"updateSalts\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]",
}

// GuardABI is the input ABI used to generate the binding from.
// Deprecated: Use GuardMetaData.ABI instead.
var GuardABI = GuardMetaData.ABI

// Guard is an auto generated Go binding around an Ethereum contract.
type Guard struct {
	GuardCaller     // Read-only binding to the contract
	GuardTransactor // Write-only binding to the contract
	GuardFilterer   // Log filterer for contract events
}

// GuardCaller is an auto generated read-only Go binding around an Ethereum contract.
type GuardCaller struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// GuardTransactor is an auto generated write-only Go binding around an Ethereum contract.
type GuardTransactor struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// GuardFilterer is an auto generated log filtering Go binding around an Ethereum contract events.
type GuardFilterer struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// GuardSession is an auto generated Go binding around an Ethereum contract,
// with pre-set call and transact options.
type GuardSession struct {
	Contract     *Guard            // Generic contract binding to set the session for
	CallOpts     bind.CallOpts     // Call options to use throughout this session
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// GuardCallerSession is an auto generated read-only Go binding around an Ethereum contract,
// with pre-set call options.
type GuardCallerSession struct {
	Contract *GuardCaller  // Generic contract caller binding to set the session for
	CallOpts bind.CallOpts // Call options to use throughout this session
}

// GuardTransactorSession is an auto generated write-only Go binding around an Ethereum contract,
// with pre-set transact options.
type GuardTransactorSession struct {
	Contract     *GuardTransactor  // Generic contract transactor binding to set the session for
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// GuardRaw is an auto generated low-level Go binding around an Ethereum contract.
type GuardRaw struct {
	Contract *Guard // Generic contract binding to access the raw methods on
}

// GuardCallerRaw is an auto generated low-level read-only Go binding around an Ethereum contract.
type GuardCallerRaw struct {
	Contract *GuardCaller // Generic read-only contract binding to access the raw methods on
}

// GuardTransactorRaw is an auto generated low-level write-only Go binding around an Ethereum contract.
type GuardTransactorRaw struct {
	Contract *GuardTransactor // Generic write-only contract binding to access the raw methods on
}

// NewGuard creates a new instance of Guard, bound to a specific deployed contract.
func NewGuard(address common.Address, backend bind.ContractBackend) (*Guard, error) {
	contract, err := bindGuard(address, backend, backend, backend)
	if err != nil {
		return nil, err
	}
	return &Guard{GuardCaller: GuardCaller{contract: contract}, GuardTransactor: GuardTransactor{contract: contract}, GuardFilterer: GuardFilterer{contract: contract}}, nil
}

// NewGuardCaller creates a new read-only instance of Guard, bound to a specific deployed contract.
func NewGuardCaller(address common.Address, caller bind.ContractCaller) (*GuardCaller, error) {
	contract, err := bindGuard(address, caller, nil, nil)
	if err != nil {
		return nil, err
	}
	return &GuardCaller{contract: contract}, nil
}

// NewGuardTransactor creates a new write-only instance of Guard, bound to a specific deployed contract.
func NewGuardTransactor(address common.Address, transactor bind.ContractTransactor) (*GuardTransactor, error) {
	contract, err := bindGuard(address, nil, transactor, nil)
	if err != nil {
		return nil, err
	}
	return &GuardTransactor{contract: contract}, nil
}

// NewGuardFilterer creates a new log filterer instance of Guard, bound to a specific deployed contract.
func NewGuardFilterer(address common.Address, filterer bind.ContractFilterer) (*GuardFilterer, error) {
	contract, err := bindGuard(address, nil, nil, filterer)
	if err != nil {
		return nil, err
	}
	return &GuardFilterer{contract: contract}, nil
}

// bindGuard binds a generic wrapper to an already deployed contract.
func bindGuard(address common.Address, caller bind.ContractCaller, transactor bind.ContractTransactor, filterer bind.ContractFilterer) (*bind.BoundContract, error) {
	parsed, err := GuardMetaData.GetAbi()
	if err != nil {
		return nil, err
	}
	return bind.NewBoundContract(address, *parsed, caller, transactor, filterer), nil
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Guard *GuardRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Guard.Contract.GuardCaller.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Guard *GuardRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Guard.Contract.GuardTransactor.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Guard *GuardRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Guard.Contract.GuardTransactor.contract.Transact(opts, method, params...)
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Guard *GuardCallerRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Guard.Contract.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Guard *GuardTransactorRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Guard.Contract.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Guard *GuardTransactorRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Guard.Contract.contract.Transact(opts, method, params...)
}

// GetSaltStatus is a free data retrieval call binding the contract method 0x27481b38.
//
// Solidity: function _getSaltStatus(address addr) view returns(uint256, bool)
func (_Guard *GuardCaller) GetSaltStatus(opts *bind.CallOpts, addr common.Address) (*big.Int, bool, error) {
	var out []interface{}
	err := _Guard.contract.Call(opts, &out, "_getSaltStatus", addr)

	if err != nil {
		return *new(*big.Int), *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)
	out1 := *abi.ConvertType(out[1], new(bool)).(*bool)

	return out0, out1, err

}

// GetSaltStatus is a free data retrieval call binding the contract method 0x27481b38.
//
// Solidity: function _getSaltStatus(address addr) view returns(uint256, bool)
func (_Guard *GuardSession) GetSaltStatus(addr common.Address) (*big.Int, bool, error) {
	return _Guard.Contract.GetSaltStatus(&_Guard.CallOpts, addr)
}

// GetSaltStatus is a free data retrieval call binding the contract method 0x27481b38.
//
// Solidity: function _getSaltStatus(address addr) view returns(uint256, bool)
func (_Guard *GuardCallerSession) GetSaltStatus(addr common.Address) (*big.Int, bool, error) {
	return _Guard.Contract.GetSaltStatus(&_Guard.CallOpts, addr)
}

// BlackList is a free data retrieval call binding the contract method 0x4838d165.
//
// Solidity: function blackList(address ) view returns(bool)
func (_Guard *GuardCaller) BlackList(opts *bind.CallOpts, arg0 common.Address) (bool, error) {
	var out []interface{}
	err := _Guard.contract.Call(opts, &out, "blackList", arg0)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// BlackList is a free data retrieval call binding the contract method 0x4838d165.
//
// Solidity: function blackList(address ) view returns(bool)
func (_Guard *GuardSession) BlackList(arg0 common.Address) (bool, error) {
	return _Guard.Contract.BlackList(&_Guard.CallOpts, arg0)
}

// BlackList is a free data retrieval call binding the contract method 0x4838d165.
//
// Solidity: function blackList(address ) view returns(bool)
func (_Guard *GuardCallerSession) BlackList(arg0 common.Address) (bool, error) {
	return _Guard.Contract.BlackList(&_Guard.CallOpts, arg0)
}

// GetSaltStatuses is a free data retrieval call binding the contract method 0xb1422015.
//
// Solidity: function getSaltStatuses(address[] addrs) view returns(uint256[], bool[])
func (_Guard *GuardCaller) GetSaltStatuses(opts *bind.CallOpts, addrs []common.Address) ([]*big.Int, []bool, error) {
	var out []interface{}
	err := _Guard.contract.Call(opts, &out, "getSaltStatuses", addrs)

	if err != nil {
		return *new([]*big.Int), *new([]bool), err
	}

	out0 := *abi.ConvertType(out[0], new([]*big.Int)).(*[]*big.Int)
	out1 := *abi.ConvertType(out[1], new([]bool)).(*[]bool)

	return out0, out1, err

}

// GetSaltStatuses is a free data retrieval call binding the contract method 0xb1422015.
//
// Solidity: function getSaltStatuses(address[] addrs) view returns(uint256[], bool[])
func (_Guard *GuardSession) GetSaltStatuses(addrs []common.Address) ([]*big.Int, []bool, error) {
	return _Guard.Contract.GetSaltStatuses(&_Guard.CallOpts, addrs)
}

// GetSaltStatuses is a free data retrieval call binding the contract method 0xb1422015.
//
// Solidity: function getSaltStatuses(address[] addrs) view returns(uint256[], bool[])
func (_Guard *GuardCallerSession) GetSaltStatuses(addrs []common.Address) ([]*big.Int, []bool, error) {
	return _Guard.Contract.GetSaltStatuses(&_Guard.CallOpts, addrs)
}

// GetUDMStatus is a free data retrieval call binding the contract method 0x21e1bec5.
//
// Solidity: function getUDMStatus() view returns(bool)
func (_Guard *GuardCaller) GetUDMStatus(opts *bind.CallOpts) (bool, error) {
	var out []interface{}
	err := _Guard.contract.Call(opts, &out, "getUDMStatus")

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// GetUDMStatus is a free data retrieval call binding the contract method 0x21e1bec5.
//
// Solidity: function getUDMStatus() view returns(bool)
func (_Guard *GuardSession) GetUDMStatus() (bool, error) {
	return _Guard.Contract.GetUDMStatus(&_Guard.CallOpts)
}

// GetUDMStatus is a free data retrieval call binding the contract method 0x21e1bec5.
//
// Solidity: function getUDMStatus() view returns(bool)
func (_Guard *GuardCallerSession) GetUDMStatus() (bool, error) {
	return _Guard.Contract.GetUDMStatus(&_Guard.CallOpts)
}

// SaltList is a free data retrieval call binding the contract method 0xb6a61b0e.
//
// Solidity: function saltList(address ) view returns(uint256)
func (_Guard *GuardCaller) SaltList(opts *bind.CallOpts, arg0 common.Address) (*big.Int, error) {
	var out []interface{}
	err := _Guard.contract.Call(opts, &out, "saltList", arg0)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// SaltList is a free data retrieval call binding the contract method 0xb6a61b0e.
//
// Solidity: function saltList(address ) view returns(uint256)
func (_Guard *GuardSession) SaltList(arg0 common.Address) (*big.Int, error) {
	return _Guard.Contract.SaltList(&_Guard.CallOpts, arg0)
}

// SaltList is a free data retrieval call binding the contract method 0xb6a61b0e.
//
// Solidity: function saltList(address ) view returns(uint256)
func (_Guard *GuardCallerSession) SaltList(arg0 common.Address) (*big.Int, error) {
	return _Guard.Contract.SaltList(&_Guard.CallOpts, arg0)
}

// BanUser is a paid mutator transaction binding the contract method 0x23a60272.
//
// Solidity: function _banUser(address addr) returns()
func (_Guard *GuardTransactor) BanUser(opts *bind.TransactOpts, addr common.Address) (*types.Transaction, error) {
	return _Guard.contract.Transact(opts, "_banUser", addr)
}

// BanUser is a paid mutator transaction binding the contract method 0x23a60272.
//
// Solidity: function _banUser(address addr) returns()
func (_Guard *GuardSession) BanUser(addr common.Address) (*types.Transaction, error) {
	return _Guard.Contract.BanUser(&_Guard.TransactOpts, addr)
}

// BanUser is a paid mutator transaction binding the contract method 0x23a60272.
//
// Solidity: function _banUser(address addr) returns()
func (_Guard *GuardTransactorSession) BanUser(addr common.Address) (*types.Transaction, error) {
	return _Guard.Contract.BanUser(&_Guard.TransactOpts, addr)
}

// RecoverUser is a paid mutator transaction binding the contract method 0x6527c19c.
//
// Solidity: function _recoverUser(address addr) returns()
func (_Guard *GuardTransactor) RecoverUser(opts *bind.TransactOpts, addr common.Address) (*types.Transaction, error) {
	return _Guard.contract.Transact(opts, "_recoverUser", addr)
}

// RecoverUser is a paid mutator transaction binding the contract method 0x6527c19c.
//
// Solidity: function _recoverUser(address addr) returns()
func (_Guard *GuardSession) RecoverUser(addr common.Address) (*types.Transaction, error) {
	return _Guard.Contract.RecoverUser(&_Guard.TransactOpts, addr)
}

// RecoverUser is a paid mutator transaction binding the contract method 0x6527c19c.
//
// Solidity: function _recoverUser(address addr) returns()
func (_Guard *GuardTransactorSession) RecoverUser(addr common.Address) (*types.Transaction, error) {
	return _Guard.Contract.RecoverUser(&_Guard.TransactOpts, addr)
}

// UpdateSalt is a paid mutator transaction binding the contract method 0x9c961ed1.
//
// Solidity: function _updateSalt(address user, uint256 salt) returns()
func (_Guard *GuardTransactor) UpdateSalt(opts *bind.TransactOpts, user common.Address, salt *big.Int) (*types.Transaction, error) {
	return _Guard.contract.Transact(opts, "_updateSalt", user, salt)
}

// UpdateSalt is a paid mutator transaction binding the contract method 0x9c961ed1.
//
// Solidity: function _updateSalt(address user, uint256 salt) returns()
func (_Guard *GuardSession) UpdateSalt(user common.Address, salt *big.Int) (*types.Transaction, error) {
	return _Guard.Contract.UpdateSalt(&_Guard.TransactOpts, user, salt)
}

// UpdateSalt is a paid mutator transaction binding the contract method 0x9c961ed1.
//
// Solidity: function _updateSalt(address user, uint256 salt) returns()
func (_Guard *GuardTransactorSession) UpdateSalt(user common.Address, salt *big.Int) (*types.Transaction, error) {
	return _Guard.Contract.UpdateSalt(&_Guard.TransactOpts, user, salt)
}

// BanUsers is a paid mutator transaction binding the contract method 0xb188c6ec.
//
// Solidity: function banUsers(address[] addrs) returns()
func (_Guard *GuardTransactor) BanUsers(opts *bind.TransactOpts, addrs []common.Address) (*types.Transaction, error) {
	return _Guard.contract.Transact(opts, "banUsers", addrs)
}

// BanUsers is a paid mutator transaction binding the contract method 0xb188c6ec.
//
// Solidity: function banUsers(address[] addrs) returns()
func (_Guard *GuardSession) BanUsers(addrs []common.Address) (*types.Transaction, error) {
	return _Guard.Contract.BanUsers(&_Guard.TransactOpts, addrs)
}

// BanUsers is a paid mutator transaction binding the contract method 0xb188c6ec.
//
// Solidity: function banUsers(address[] addrs) returns()
func (_Guard *GuardTransactorSession) BanUsers(addrs []common.Address) (*types.Transaction, error) {
	return _Guard.Contract.BanUsers(&_Guard.TransactOpts, addrs)
}

// ChangeOwner is a paid mutator transaction binding the contract method 0xa6f9dae1.
//
// Solidity: function changeOwner(address _newOwner) returns()
func (_Guard *GuardTransactor) ChangeOwner(opts *bind.TransactOpts, _newOwner common.Address) (*types.Transaction, error) {
	return _Guard.contract.Transact(opts, "changeOwner", _newOwner)
}

// ChangeOwner is a paid mutator transaction binding the contract method 0xa6f9dae1.
//
// Solidity: function changeOwner(address _newOwner) returns()
func (_Guard *GuardSession) ChangeOwner(_newOwner common.Address) (*types.Transaction, error) {
	return _Guard.Contract.ChangeOwner(&_Guard.TransactOpts, _newOwner)
}

// ChangeOwner is a paid mutator transaction binding the contract method 0xa6f9dae1.
//
// Solidity: function changeOwner(address _newOwner) returns()
func (_Guard *GuardTransactorSession) ChangeOwner(_newOwner common.Address) (*types.Transaction, error) {
	return _Guard.Contract.ChangeOwner(&_Guard.TransactOpts, _newOwner)
}

// ChangeUDMStatus is a paid mutator transaction binding the contract method 0x5c20ece5.
//
// Solidity: function changeUDMStatus() returns()
func (_Guard *GuardTransactor) ChangeUDMStatus(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Guard.contract.Transact(opts, "changeUDMStatus")
}

// ChangeUDMStatus is a paid mutator transaction binding the contract method 0x5c20ece5.
//
// Solidity: function changeUDMStatus() returns()
func (_Guard *GuardSession) ChangeUDMStatus() (*types.Transaction, error) {
	return _Guard.Contract.ChangeUDMStatus(&_Guard.TransactOpts)
}

// ChangeUDMStatus is a paid mutator transaction binding the contract method 0x5c20ece5.
//
// Solidity: function changeUDMStatus() returns()
func (_Guard *GuardTransactorSession) ChangeUDMStatus() (*types.Transaction, error) {
	return _Guard.Contract.ChangeUDMStatus(&_Guard.TransactOpts)
}

// RecoverUsers is a paid mutator transaction binding the contract method 0x8584f4b4.
//
// Solidity: function recoverUsers(address[] addrs) returns()
func (_Guard *GuardTransactor) RecoverUsers(opts *bind.TransactOpts, addrs []common.Address) (*types.Transaction, error) {
	return _Guard.contract.Transact(opts, "recoverUsers", addrs)
}

// RecoverUsers is a paid mutator transaction binding the contract method 0x8584f4b4.
//
// Solidity: function recoverUsers(address[] addrs) returns()
func (_Guard *GuardSession) RecoverUsers(addrs []common.Address) (*types.Transaction, error) {
	return _Guard.Contract.RecoverUsers(&_Guard.TransactOpts, addrs)
}

// RecoverUsers is a paid mutator transaction binding the contract method 0x8584f4b4.
//
// Solidity: function recoverUsers(address[] addrs) returns()
func (_Guard *GuardTransactorSession) RecoverUsers(addrs []common.Address) (*types.Transaction, error) {
	return _Guard.Contract.RecoverUsers(&_Guard.TransactOpts, addrs)
}

// UpdateSalts is a paid mutator transaction binding the contract method 0xf8574768.
//
// Solidity: function updateSalts(address[] users, uint256[] salts) returns()
func (_Guard *GuardTransactor) UpdateSalts(opts *bind.TransactOpts, users []common.Address, salts []*big.Int) (*types.Transaction, error) {
	return _Guard.contract.Transact(opts, "updateSalts", users, salts)
}

// UpdateSalts is a paid mutator transaction binding the contract method 0xf8574768.
//
// Solidity: function updateSalts(address[] users, uint256[] salts) returns()
func (_Guard *GuardSession) UpdateSalts(users []common.Address, salts []*big.Int) (*types.Transaction, error) {
	return _Guard.Contract.UpdateSalts(&_Guard.TransactOpts, users, salts)
}

// UpdateSalts is a paid mutator transaction binding the contract method 0xf8574768.
//
// Solidity: function updateSalts(address[] users, uint256[] salts) returns()
func (_Guard *GuardTransactorSession) UpdateSalts(users []common.Address, salts []*big.Int) (*types.Transaction, error) {
	return _Guard.Contract.UpdateSalts(&_Guard.TransactOpts, users, salts)
}
