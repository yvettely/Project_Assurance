pragma solidity ^0.5.0;

import "./WoofCoin.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";

//  Inherit the crowdsale contracts
contract AssuranceCharity is Crowdsale, MintedCrowdsale {

    constructor(
        address payable wallet,
        WoofCoin token,
        uint rate
        )
        
        Crowdsale(rate, wallet, token)
        MintedCrowdsale()
        public {
        // constructor can stay empty
    }
}

contract AssuranceCharitySaleDeployer {
    // Instantiate variables
    address public tokenCharityAddress;
    address public tokenAddress;

    constructor(
        string memory name,
        string memory symbol,
        address payable wallet
        )
        
        public
        
        {

        // create the WoofCoin
        WoofCoin token = new WoofCoin(name, symbol, 0);
        tokenAddress = address(token);
        
       
        AssuranceCharity assurance_sale = new AssuranceCharity(wallet, token, 1);
        tokenCharityAddress = address(assurance_sale);

        // make the AssuranceCharity contract a minter, 
        // then have the AssuranceCharitySaleDeployer renounce its minter role
        token.addMinter(tokenCharityAddress);
        token.renounceMinter();
    }
}