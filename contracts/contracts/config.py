abi = [
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			}
		],
		"name": "_banUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			}
		],
		"name": "_getSaltStatus",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			}
		],
		"name": "_recoverUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "salt",
				"type": "uint256"
			}
		],
		"name": "_updateSalt",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address[]",
				"name": "addrs",
				"type": "address[]"
			}
		],
		"name": "banUsers",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "blackList",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_newOwner",
				"type": "address"
			}
		],
		"name": "changeOwner",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "changeUDMStatus",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address[]",
				"name": "addrs",
				"type": "address[]"
			}
		],
		"name": "getSaltStatuses",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			},
			{
				"internalType": "bool[]",
				"name": "",
				"type": "bool[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getUDMStatus",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address[]",
				"name": "addrs",
				"type": "address[]"
			}
		],
		"name": "recoverUsers",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "saltList",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address[]",
				"name": "users",
				"type": "address[]"
			},
			{
				"internalType": "uint256[]",
				"name": "salts",
				"type": "uint256[]"
			}
		],
		"name": "updateSalts",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

bytecode = "608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550611604806100606000396000f3fe608060405234801561001057600080fd5b50600436106100cf5760003560e01c80638584f4b41161008c578063b142201511610066578063b1422015146101e9578063b188c6ec1461021a578063b6a61b0e14610236578063f857476814610266576100cf565b80638584f4b4146101955780639c961ed1146101b1578063a6f9dae1146101cd576100cf565b806321e1bec5146100d457806323a60272146100f257806327481b381461010e5780634838d1651461013f5780635c20ece51461016f5780636527c19c14610179575b600080fd5b6100dc610282565b6040516100e99190611291565b60405180910390f35b61010c60048036038101906101079190610f64565b610298565b005b61012860048036038101906101239190610f64565b610486565b604051610136929190611367565b60405180910390f35b61015960048036038101906101549190610f64565b61052b565b6040516101669190611291565b60405180910390f35b61017761054b565b005b610193600480360381019061018e9190610f64565b610605565b005b6101af60048036038101906101aa9190610fc9565b6107f4565b005b6101cb60048036038101906101c69190610f8d565b610870565b005b6101e760048036038101906101e29190610f64565b6109b8565b005b61020360048036038101906101fe9190610fc9565b610afb565b60405161021192919061125a565b60405180910390f35b610234600480360381019061022f9190610fc9565b610d0c565b005b610250600480360381019061024b9190610f64565b610d88565b60405161025d919061134c565b60405180910390f35b610280600480360381019061027b919061100e565b610da0565b005b60008060149054906101000a900460ff16905090565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610326576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161031d906112ec565b60405180910390fd5b80600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff161415610397576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161038e9061130c565b60405180910390fd5b60011515600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff161515141561042b576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016104229061132c565b60405180910390fd5b60018060008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055505050565b6000806000600260008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205490506000600160008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1690508181935093505050915091565b60016020528060005260406000206000915054906101000a900460ff1681565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146105d9576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105d0906112ec565b60405180910390fd5b600060149054906101000a900460ff1615600060146101000a81548160ff021916908315150217905550565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610693576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161068a906112ec565b60405180910390fd5b80600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff161415610704576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016106fb9061130c565b60405180910390fd5b60001515600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1615151415610798576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161078f906112cc565b60405180910390fd5b6000600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055505050565b60005b8282905081101561086b5761085883838381811061083e577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b90506020020160208101906108539190610f64565b610605565b80806108639061145b565b9150506107f7565b505050565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146108fe576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016108f5906112ec565b60405180910390fd5b81600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff16141561096f576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016109669061130c565b60405180910390fd5b81600260008573ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550505050565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610a46576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610a3d906112ec565b60405180910390fd5b80600073ffffffffffffffffffffffffffffffffffffffff168173ffffffffffffffffffffffffffffffffffffffff161415610ab7576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610aae9061130c565b60405180910390fd5b816000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505050565b60608060008484905067ffffffffffffffff811115610b43577f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b604051908082528060200260200182016040528015610b715781602001602082028036833780820191505090505b50905060008585905067ffffffffffffffff811115610bb9577f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b604051908082528060200260200182016040528015610be75781602001602082028036833780820191505090505b50905060005b86869050811015610cfc57600080610c51898985818110610c37577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b9050602002016020810190610c4c9190610f64565b610486565b9150915081858481518110610c8f577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b60200260200101818152505080848481518110610cd5577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b60200260200101901515908115158152505050508080610cf49061145b565b915050610bed565b5081819350935050509250929050565b60005b82829050811015610d8357610d70838383818110610d56577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b9050602002016020810190610d6b9190610f64565b610298565b8080610d7b9061145b565b915050610d0f565b505050565b60026020528060005260406000206000915090505481565b818190508484905014610de8576040517f08c379a0000000000000000000000000000000000000000000000000000000008152600401610ddf906112ac565b60405180910390fd5b60005b84849050811015610e9f57610e8c858583818110610e32577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b9050602002016020810190610e479190610f64565b848484818110610e80577f4e487b7100000000000000000000000000000000000000000000000000000000600052603260045260246000fd5b90506020020135610870565b8080610e979061145b565b915050610deb565b5050505050565b600081359050610eb5816115a0565b92915050565b60008083601f840112610ecd57600080fd5b8235905067ffffffffffffffff811115610ee657600080fd5b602083019150836020820283011115610efe57600080fd5b9250929050565b60008083601f840112610f1757600080fd5b8235905067ffffffffffffffff811115610f3057600080fd5b602083019150836020820283011115610f4857600080fd5b9250929050565b600081359050610f5e816115b7565b92915050565b600060208284031215610f7657600080fd5b6000610f8484828501610ea6565b91505092915050565b60008060408385031215610fa057600080fd5b6000610fae85828601610ea6565b9250506020610fbf85828601610f4f565b9150509250929050565b60008060208385031215610fdc57600080fd5b600083013567ffffffffffffffff811115610ff657600080fd5b61100285828601610ebb565b92509250509250929050565b6000806000806040858703121561102457600080fd5b600085013567ffffffffffffffff81111561103e57600080fd5b61104a87828801610ebb565b9450945050602085013567ffffffffffffffff81111561106957600080fd5b61107587828801610f05565b925092505092959194509250565b600061108f838361116f565b60208301905092915050565b60006110a7838361123c565b60208301905092915050565b60006110be826113b0565b6110c881856113e0565b93506110d383611390565b8060005b838110156111045781516110eb8882611083565b97506110f6836113c6565b9250506001810190506110d7565b5085935050505092915050565b600061111c826113bb565b61112681856113f1565b9350611131836113a0565b8060005b83811015611162578151611149888261109b565b9750611154836113d3565b925050600181019050611135565b5085935050505092915050565b61117881611425565b82525050565b61118781611425565b82525050565b600061119a601983611402565b91506111a5826114d3565b602082019050919050565b60006111bd601183611402565b91506111c8826114fc565b602082019050919050565b60006111e0600983611402565b91506111eb82611525565b602082019050919050565b6000611203601183611402565b915061120e8261154e565b602082019050919050565b6000611226600e83611402565b915061123182611577565b602082019050919050565b61124581611451565b82525050565b61125481611451565b82525050565b600060408201905081810360008301526112748185611111565b9050818103602083015261128881846110b3565b90509392505050565b60006020820190506112a6600083018461117e565b92915050565b600060208201905081810360008301526112c58161118d565b9050919050565b600060208201905081810360008301526112e5816111b0565b9050919050565b60006020820190508181036000830152611305816111d3565b9050919050565b60006020820190508181036000830152611325816111f6565b9050919050565b6000602082019050818103600083015261134581611219565b9050919050565b6000602082019050611361600083018461124b565b92915050565b600060408201905061137c600083018561124b565b611389602083018461117e565b9392505050565b6000819050602082019050919050565b6000819050602082019050919050565b600081519050919050565b600081519050919050565b6000602082019050919050565b6000602082019050919050565b600082825260208201905092915050565b600082825260208201905092915050565b600082825260208201905092915050565b600061141e82611431565b9050919050565b60008115159050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b600061146682611451565b91507fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff821415611499576114986114a4565b5b600182019050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b7f496e707574206c656e67746820697320646966666572656e7400000000000000600082015250565b7f416c7265616479207265636f7665726564000000000000000000000000000000600082015250565b7f4e6f74206f776e65720000000000000000000000000000000000000000000000600082015250565b7f4e6f742076616c69642061646472657373000000000000000000000000000000600082015250565b7f416c72656164792042616e6e6564000000000000000000000000000000000000600082015250565b6115a981611413565b81146115b457600080fd5b50565b6115c081611451565b81146115cb57600080fd5b5056fea26469706673582212207eca5d37390ab2841976f7b40cf2d5126ffff4fe7f73ead2cf07a4aed33c17c164736f6c63430008040033"