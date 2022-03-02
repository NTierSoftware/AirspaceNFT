// @author John Donaldson, N-Tier Software Engineering
// SPDX-License-Identifier: MIT

//pragma solidity >=0.6.0 <0.8.0;
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
//import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract AirspaceNFT is ERC721URIStorage, Ownable {
    uint256 public tokenCounter = 0;

    event createdCollectible(uint256 indexed tokenId, address requester);

    constructor () public ERC721 ("Airspace TEST4", "AIRS") {}

    function createCollectible(string memory tokenURI) public onlyOwner returns (uint256) {
        ++tokenCounter;
        _safeMint(msg.sender, tokenCounter);
        setTokenURI(tokenCounter, tokenURI);
        emit createdCollectible(tokenCounter, msg.sender);
        return tokenCounter;
    }


    function setTokenURI(uint256 tokenId, string memory _tokenURI) public onlyOwner {
//        require(_isApprovedOrOwner(_msgSender(), tokenId), "setTokenURI(): caller is not owner nor approved");
        _setTokenURI(tokenId, _tokenURI);
    }

    function burn(uint256 tokenId) public onlyOwner {
        if (_exists(tokenId))
            _burn(tokenId);
    }
}
