// Code generated - DO NOT EDIT.
// This file is a generated binding and any manual changes will be lost.

package guardtest

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

// GuardtestMetaData contains all meta data concerning the Guardtest contract.
var GuardtestMetaData = &bind.MetaData{
	ABI: "[{\"inputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"addr\",\"type\":\"uint256\"}],\"name\":\"_banUser\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"addr\",\"type\":\"uint256\"}],\"name\":\"_getSaltStatus\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"},{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"addr\",\"type\":\"uint256\"}],\"name\":\"_recoverUser\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"user\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"salt\",\"type\":\"uint256\"}],\"name\":\"_updateSalt\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256[]\",\"name\":\"addrs\",\"type\":\"uint256[]\"}],\"name\":\"banUsers\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"name\":\"blackList\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"_newOwner\",\"type\":\"address\"}],\"name\":\"changeOwner\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"changeUDMStatus\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256[]\",\"name\":\"addrs\",\"type\":\"uint256[]\"}],\"name\":\"getSaltStatuses\",\"outputs\":[{\"internalType\":\"uint256[]\",\"name\":\"\",\"type\":\"uint256[]\"},{\"internalType\":\"bool[]\",\"name\":\"\",\"type\":\"bool[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getUDMStatus\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256[]\",\"name\":\"addrs\",\"type\":\"uint256[]\"}],\"name\":\"recoverUsers\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"name\":\"saltList\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256[]\",\"name\":\"users\",\"type\":\"uint256[]\"},{\"internalType\":\"uint256[]\",\"name\":\"salts\",\"type\":\"uint256[]\"}],\"name\":\"updateSalts\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]",
}

// GuardtestABI is the input ABI used to generate the binding from.
// Deprecated: Use GuardtestMetaData.ABI instead.
var GuardtestABI = GuardtestMetaData.ABI

// Guardtest is an auto generated Go binding around an Ethereum contract.
type Guardtest struct {
	GuardtestCaller     // Read-only binding to the contract
	GuardtestTransactor // Write-only binding to the contract
	GuardtestFilterer   // Log filterer for contract events
}

// GuardtestCaller is an auto generated read-only Go binding around an Ethereum contract.
type GuardtestCaller struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// GuardtestTransactor is an auto generated write-only Go binding around an Ethereum contract.
type GuardtestTransactor struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// GuardtestFilterer is an auto generated log filtering Go binding around an Ethereum contract events.
type GuardtestFilterer struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// GuardtestSession is an auto generated Go binding around an Ethereum contract,
// with pre-set call and transact options.
type GuardtestSession struct {
	Contract     *Guardtest        // Generic contract binding to set the session for
	CallOpts     bind.CallOpts     // Call options to use throughout this session
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// GuardtestCallerSession is an auto generated read-only Go binding around an Ethereum contract,
// with pre-set call options.
type GuardtestCallerSession struct {
	Contract *GuardtestCaller // Generic contract caller binding to set the session for
	CallOpts bind.CallOpts    // Call options to use throughout this session
}

// GuardtestTransactorSession is an auto generated write-only Go binding around an Ethereum contract,
// with pre-set transact options.
type GuardtestTransactorSession struct {
	Contract     *GuardtestTransactor // Generic contract transactor binding to set the session for
	TransactOpts bind.TransactOpts    // Transaction auth options to use throughout this session
}

// GuardtestRaw is an auto generated low-level Go binding around an Ethereum contract.
type GuardtestRaw struct {
	Contract *Guardtest // Generic contract binding to access the raw methods on
}

// GuardtestCallerRaw is an auto generated low-level read-only Go binding around an Ethereum contract.
type GuardtestCallerRaw struct {
	Contract *GuardtestCaller // Generic read-only contract binding to access the raw methods on
}

// GuardtestTransactorRaw is an auto generated low-level write-only Go binding around an Ethereum contract.
type GuardtestTransactorRaw struct {
	Contract *GuardtestTransactor // Generic write-only contract binding to access the raw methods on
}

// NewGuardtest creates a new instance of Guardtest, bound to a specific deployed contract.
func NewGuardtest(address common.Address, backend bind.ContractBackend) (*Guardtest, error) {
	contract, err := bindGuardtest(address, backend, backend, backend)
	if err != nil {
		return nil, err
	}
	return &Guardtest{GuardtestCaller: GuardtestCaller{contract: contract}, GuardtestTransactor: GuardtestTransactor{contract: contract}, GuardtestFilterer: GuardtestFilterer{contract: contract}}, nil
}

// NewGuardtestCaller creates a new read-only instance of Guardtest, bound to a specific deployed contract.
func NewGuardtestCaller(address common.Address, caller bind.ContractCaller) (*GuardtestCaller, error) {
	contract, err := bindGuardtest(address, caller, nil, nil)
	if err != nil {
		return nil, err
	}
	return &GuardtestCaller{contract: contract}, nil
}

// NewGuardtestTransactor creates a new write-only instance of Guardtest, bound to a specific deployed contract.
func NewGuardtestTransactor(address common.Address, transactor bind.ContractTransactor) (*GuardtestTransactor, error) {
	contract, err := bindGuardtest(address, nil, transactor, nil)
	if err != nil {
		return nil, err
	}
	return &GuardtestTransactor{contract: contract}, nil
}

// NewGuardtestFilterer creates a new log filterer instance of Guardtest, bound to a specific deployed contract.
func NewGuardtestFilterer(address common.Address, filterer bind.ContractFilterer) (*GuardtestFilterer, error) {
	contract, err := bindGuardtest(address, nil, nil, filterer)
	if err != nil {
		return nil, err
	}
	return &GuardtestFilterer{contract: contract}, nil
}

// bindGuardtest binds a generic wrapper to an already deployed contract.
func bindGuardtest(address common.Address, caller bind.ContractCaller, transactor bind.ContractTransactor, filterer bind.ContractFilterer) (*bind.BoundContract, error) {
	parsed, err := GuardtestMetaData.GetAbi()
	if err != nil {
		return nil, err
	}
	return bind.NewBoundContract(address, *parsed, caller, transactor, filterer), nil
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Guardtest *GuardtestRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Guardtest.Contract.GuardtestCaller.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Guardtest *GuardtestRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Guardtest.Contract.GuardtestTransactor.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Guardtest *GuardtestRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Guardtest.Contract.GuardtestTransactor.contract.Transact(opts, method, params...)
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Guardtest *GuardtestCallerRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Guardtest.Contract.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Guardtest *GuardtestTransactorRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Guardtest.Contract.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Guardtest *GuardtestTransactorRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Guardtest.Contract.contract.Transact(opts, method, params...)
}

// GetSaltStatus is a free data retrieval call binding the contract method 0x3af4f001.
//
// Solidity: function _getSaltStatus(uint256 addr) view returns(uint256, bool)
func (_Guardtest *GuardtestCaller) GetSaltStatus(opts *bind.CallOpts, addr *big.Int) (*big.Int, bool, error) {
	var out []interface{}
	err := _Guardtest.contract.Call(opts, &out, "_getSaltStatus", addr)

	if err != nil {
		return *new(*big.Int), *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)
	out1 := *abi.ConvertType(out[1], new(bool)).(*bool)

	return out0, out1, err

}

// GetSaltStatus is a free data retrieval call binding the contract method 0x3af4f001.
//
// Solidity: function _getSaltStatus(uint256 addr) view returns(uint256, bool)
func (_Guardtest *GuardtestSession) GetSaltStatus(addr *big.Int) (*big.Int, bool, error) {
	return _Guardtest.Contract.GetSaltStatus(&_Guardtest.CallOpts, addr)
}

// GetSaltStatus is a free data retrieval call binding the contract method 0x3af4f001.
//
// Solidity: function _getSaltStatus(uint256 addr) view returns(uint256, bool)
func (_Guardtest *GuardtestCallerSession) GetSaltStatus(addr *big.Int) (*big.Int, bool, error) {
	return _Guardtest.Contract.GetSaltStatus(&_Guardtest.CallOpts, addr)
}

// BlackList is a free data retrieval call binding the contract method 0x709ec8b4.
//
// Solidity: function blackList(uint256 ) view returns(bool)
func (_Guardtest *GuardtestCaller) BlackList(opts *bind.CallOpts, arg0 *big.Int) (bool, error) {
	var out []interface{}
	err := _Guardtest.contract.Call(opts, &out, "blackList", arg0)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// BlackList is a free data retrieval call binding the contract method 0x709ec8b4.
//
// Solidity: function blackList(uint256 ) view returns(bool)
func (_Guardtest *GuardtestSession) BlackList(arg0 *big.Int) (bool, error) {
	return _Guardtest.Contract.BlackList(&_Guardtest.CallOpts, arg0)
}

// BlackList is a free data retrieval call binding the contract method 0x709ec8b4.
//
// Solidity: function blackList(uint256 ) view returns(bool)
func (_Guardtest *GuardtestCallerSession) BlackList(arg0 *big.Int) (bool, error) {
	return _Guardtest.Contract.BlackList(&_Guardtest.CallOpts, arg0)
}

// GetSaltStatuses is a free data retrieval call binding the contract method 0x2e588fb9.
//
// Solidity: function getSaltStatuses(uint256[] addrs) view returns(uint256[], bool[])
func (_Guardtest *GuardtestCaller) GetSaltStatuses(opts *bind.CallOpts, addrs []*big.Int) ([]*big.Int, []bool, error) {
	var out []interface{}
	err := _Guardtest.contract.Call(opts, &out, "getSaltStatuses", addrs)

	if err != nil {
		return *new([]*big.Int), *new([]bool), err
	}

	out0 := *abi.ConvertType(out[0], new([]*big.Int)).(*[]*big.Int)
	out1 := *abi.ConvertType(out[1], new([]bool)).(*[]bool)

	return out0, out1, err

}

// GetSaltStatuses is a free data retrieval call binding the contract method 0x2e588fb9.
//
// Solidity: function getSaltStatuses(uint256[] addrs) view returns(uint256[], bool[])
func (_Guardtest *GuardtestSession) GetSaltStatuses(addrs []*big.Int) ([]*big.Int, []bool, error) {
	return _Guardtest.Contract.GetSaltStatuses(&_Guardtest.CallOpts, addrs)
}

// GetSaltStatuses is a free data retrieval call binding the contract method 0x2e588fb9.
//
// Solidity: function getSaltStatuses(uint256[] addrs) view returns(uint256[], bool[])
func (_Guardtest *GuardtestCallerSession) GetSaltStatuses(addrs []*big.Int) ([]*big.Int, []bool, error) {
	return _Guardtest.Contract.GetSaltStatuses(&_Guardtest.CallOpts, addrs)
}

// GetUDMStatus is a free data retrieval call binding the contract method 0x21e1bec5.
//
// Solidity: function getUDMStatus() view returns(bool)
func (_Guardtest *GuardtestCaller) GetUDMStatus(opts *bind.CallOpts) (bool, error) {
	var out []interface{}
	err := _Guardtest.contract.Call(opts, &out, "getUDMStatus")

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// GetUDMStatus is a free data retrieval call binding the contract method 0x21e1bec5.
//
// Solidity: function getUDMStatus() view returns(bool)
func (_Guardtest *GuardtestSession) GetUDMStatus() (bool, error) {
	return _Guardtest.Contract.GetUDMStatus(&_Guardtest.CallOpts)
}

// GetUDMStatus is a free data retrieval call binding the contract method 0x21e1bec5.
//
// Solidity: function getUDMStatus() view returns(bool)
func (_Guardtest *GuardtestCallerSession) GetUDMStatus() (bool, error) {
	return _Guardtest.Contract.GetUDMStatus(&_Guardtest.CallOpts)
}

// SaltList is a free data retrieval call binding the contract method 0xf3b72921.
//
// Solidity: function saltList(uint256 ) view returns(uint256)
func (_Guardtest *GuardtestCaller) SaltList(opts *bind.CallOpts, arg0 *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _Guardtest.contract.Call(opts, &out, "saltList", arg0)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// SaltList is a free data retrieval call binding the contract method 0xf3b72921.
//
// Solidity: function saltList(uint256 ) view returns(uint256)
func (_Guardtest *GuardtestSession) SaltList(arg0 *big.Int) (*big.Int, error) {
	return _Guardtest.Contract.SaltList(&_Guardtest.CallOpts, arg0)
}

// SaltList is a free data retrieval call binding the contract method 0xf3b72921.
//
// Solidity: function saltList(uint256 ) view returns(uint256)
func (_Guardtest *GuardtestCallerSession) SaltList(arg0 *big.Int) (*big.Int, error) {
	return _Guardtest.Contract.SaltList(&_Guardtest.CallOpts, arg0)
}

// BanUser is a paid mutator transaction binding the contract method 0xb6cf1577.
//
// Solidity: function _banUser(uint256 addr) returns()
func (_Guardtest *GuardtestTransactor) BanUser(opts *bind.TransactOpts, addr *big.Int) (*types.Transaction, error) {
	return _Guardtest.contract.Transact(opts, "_banUser", addr)
}

// BanUser is a paid mutator transaction binding the contract method 0xb6cf1577.
//
// Solidity: function _banUser(uint256 addr) returns()
func (_Guardtest *GuardtestSession) BanUser(addr *big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.BanUser(&_Guardtest.TransactOpts, addr)
}

// BanUser is a paid mutator transaction binding the contract method 0xb6cf1577.
//
// Solidity: function _banUser(uint256 addr) returns()
func (_Guardtest *GuardtestTransactorSession) BanUser(addr *big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.BanUser(&_Guardtest.TransactOpts, addr)
}

// RecoverUser is a paid mutator transaction binding the contract method 0xd2942d9a.
//
// Solidity: function _recoverUser(uint256 addr) returns()
func (_Guardtest *GuardtestTransactor) RecoverUser(opts *bind.TransactOpts, addr *big.Int) (*types.Transaction, error) {
	return _Guardtest.contract.Transact(opts, "_recoverUser", addr)
}

// RecoverUser is a paid mutator transaction binding the contract method 0xd2942d9a.
//
// Solidity: function _recoverUser(uint256 addr) returns()
func (_Guardtest *GuardtestSession) RecoverUser(addr *big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.RecoverUser(&_Guardtest.TransactOpts, addr)
}

// RecoverUser is a paid mutator transaction binding the contract method 0xd2942d9a.
//
// Solidity: function _recoverUser(uint256 addr) returns()
func (_Guardtest *GuardtestTransactorSession) RecoverUser(addr *big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.RecoverUser(&_Guardtest.TransactOpts, addr)
}

// UpdateSalt is a paid mutator transaction binding the contract method 0x26b9bbb0.
//
// Solidity: function _updateSalt(uint256 user, uint256 salt) returns()
func (_Guardtest *GuardtestTransactor) UpdateSalt(opts *bind.TransactOpts, user *big.Int, salt *big.Int) (*types.Transaction, error) {
	return _Guardtest.contract.Transact(opts, "_updateSalt", user, salt)
}

// UpdateSalt is a paid mutator transaction binding the contract method 0x26b9bbb0.
//
// Solidity: function _updateSalt(uint256 user, uint256 salt) returns()
func (_Guardtest *GuardtestSession) UpdateSalt(user *big.Int, salt *big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.UpdateSalt(&_Guardtest.TransactOpts, user, salt)
}

// UpdateSalt is a paid mutator transaction binding the contract method 0x26b9bbb0.
//
// Solidity: function _updateSalt(uint256 user, uint256 salt) returns()
func (_Guardtest *GuardtestTransactorSession) UpdateSalt(user *big.Int, salt *big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.UpdateSalt(&_Guardtest.TransactOpts, user, salt)
}

// BanUsers is a paid mutator transaction binding the contract method 0x10d5bb51.
//
// Solidity: function banUsers(uint256[] addrs) returns()
func (_Guardtest *GuardtestTransactor) BanUsers(opts *bind.TransactOpts, addrs []*big.Int) (*types.Transaction, error) {
	return _Guardtest.contract.Transact(opts, "banUsers", addrs)
}

// BanUsers is a paid mutator transaction binding the contract method 0x10d5bb51.
//
// Solidity: function banUsers(uint256[] addrs) returns()
func (_Guardtest *GuardtestSession) BanUsers(addrs []*big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.BanUsers(&_Guardtest.TransactOpts, addrs)
}

// BanUsers is a paid mutator transaction binding the contract method 0x10d5bb51.
//
// Solidity: function banUsers(uint256[] addrs) returns()
func (_Guardtest *GuardtestTransactorSession) BanUsers(addrs []*big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.BanUsers(&_Guardtest.TransactOpts, addrs)
}

// ChangeOwner is a paid mutator transaction binding the contract method 0xa6f9dae1.
//
// Solidity: function changeOwner(address _newOwner) returns()
func (_Guardtest *GuardtestTransactor) ChangeOwner(opts *bind.TransactOpts, _newOwner common.Address) (*types.Transaction, error) {
	return _Guardtest.contract.Transact(opts, "changeOwner", _newOwner)
}

// ChangeOwner is a paid mutator transaction binding the contract method 0xa6f9dae1.
//
// Solidity: function changeOwner(address _newOwner) returns()
func (_Guardtest *GuardtestSession) ChangeOwner(_newOwner common.Address) (*types.Transaction, error) {
	return _Guardtest.Contract.ChangeOwner(&_Guardtest.TransactOpts, _newOwner)
}

// ChangeOwner is a paid mutator transaction binding the contract method 0xa6f9dae1.
//
// Solidity: function changeOwner(address _newOwner) returns()
func (_Guardtest *GuardtestTransactorSession) ChangeOwner(_newOwner common.Address) (*types.Transaction, error) {
	return _Guardtest.Contract.ChangeOwner(&_Guardtest.TransactOpts, _newOwner)
}

// ChangeUDMStatus is a paid mutator transaction binding the contract method 0x5c20ece5.
//
// Solidity: function changeUDMStatus() returns()
func (_Guardtest *GuardtestTransactor) ChangeUDMStatus(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Guardtest.contract.Transact(opts, "changeUDMStatus")
}

// ChangeUDMStatus is a paid mutator transaction binding the contract method 0x5c20ece5.
//
// Solidity: function changeUDMStatus() returns()
func (_Guardtest *GuardtestSession) ChangeUDMStatus() (*types.Transaction, error) {
	return _Guardtest.Contract.ChangeUDMStatus(&_Guardtest.TransactOpts)
}

// ChangeUDMStatus is a paid mutator transaction binding the contract method 0x5c20ece5.
//
// Solidity: function changeUDMStatus() returns()
func (_Guardtest *GuardtestTransactorSession) ChangeUDMStatus() (*types.Transaction, error) {
	return _Guardtest.Contract.ChangeUDMStatus(&_Guardtest.TransactOpts)
}

// RecoverUsers is a paid mutator transaction binding the contract method 0xd9ba13df.
//
// Solidity: function recoverUsers(uint256[] addrs) returns()
func (_Guardtest *GuardtestTransactor) RecoverUsers(opts *bind.TransactOpts, addrs []*big.Int) (*types.Transaction, error) {
	return _Guardtest.contract.Transact(opts, "recoverUsers", addrs)
}

// RecoverUsers is a paid mutator transaction binding the contract method 0xd9ba13df.
//
// Solidity: function recoverUsers(uint256[] addrs) returns()
func (_Guardtest *GuardtestSession) RecoverUsers(addrs []*big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.RecoverUsers(&_Guardtest.TransactOpts, addrs)
}

// RecoverUsers is a paid mutator transaction binding the contract method 0xd9ba13df.
//
// Solidity: function recoverUsers(uint256[] addrs) returns()
func (_Guardtest *GuardtestTransactorSession) RecoverUsers(addrs []*big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.RecoverUsers(&_Guardtest.TransactOpts, addrs)
}

// UpdateSalts is a paid mutator transaction binding the contract method 0x7aa9a7ed.
//
// Solidity: function updateSalts(uint256[] users, uint256[] salts) returns()
func (_Guardtest *GuardtestTransactor) UpdateSalts(opts *bind.TransactOpts, users []*big.Int, salts []*big.Int) (*types.Transaction, error) {
	return _Guardtest.contract.Transact(opts, "updateSalts", users, salts)
}

// UpdateSalts is a paid mutator transaction binding the contract method 0x7aa9a7ed.
//
// Solidity: function updateSalts(uint256[] users, uint256[] salts) returns()
func (_Guardtest *GuardtestSession) UpdateSalts(users []*big.Int, salts []*big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.UpdateSalts(&_Guardtest.TransactOpts, users, salts)
}

// UpdateSalts is a paid mutator transaction binding the contract method 0x7aa9a7ed.
//
// Solidity: function updateSalts(uint256[] users, uint256[] salts) returns()
func (_Guardtest *GuardtestTransactorSession) UpdateSalts(users []*big.Int, salts []*big.Int) (*types.Transaction, error) {
	return _Guardtest.Contract.UpdateSalts(&_Guardtest.TransactOpts, users, salts)
}
