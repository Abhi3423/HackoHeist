import React, { Component } from 'react';
import Web3 from 'web3';
import './App.css';
import Meme from '../abis/Meme.json'

const ipfsClient = require('ipfs-http-client')
const ipfs = ipfsClient({ host: 'ipfs.infura.io', port: 5001, protocol: 'https' }) // leaving out the arguments will default to these values

class App extends Component {

  // async componentWillMount() {
  //   await this.loadWeb3()
  //   await this.loadBlockchainData()
  // }

  // async loadWeb3() {
  //   if (window.ethereum) {
  //     window.web3 = new Web3(window.ethereum)
  //     await window.ethereum.enable()
  //   }
  //   else if (window.web3) {
  //     window.web3 = new Web3(window.web3.currentProvider)
  //   }
  //   else {
  //     window.alert('Non-Ethereum browser detected. You should consider trying MetaMask!')
  //   }
  // }

  // async loadBlockchainData() {
  //   const web3 = window.web3
  //   // Load account
  //   const accounts = await web3.eth.getAccounts()
  //   this.setState({ account: accounts[0] })
  //   const networkId = await web3.eth.net.getId()
  //   const networkData = Meme.networks[networkId]
  //   if(networkData) {
  //     const contract = web3.eth.Contract(Meme.abi, networkData.address)
  //     this.setState({ contract })
  //     const memeHash = await contract.methods.get().call()
  //     this.setState({ memeHash })
  //   } else {
  //     window.alert('Smart contract not deployed to detected network.')
  //   }
  // }

  constructor(props) {
    super(props)

    this.state = {
      memeHash: '',
      contract: null,
      web3: null,
      buffer: null,
      account: null
    }
  }

  captureFile = (event) => {
    event.preventDefault()
    const file = event.target.files[0]
    const reader = new window.FileReader()
    reader.readAsArrayBuffer(file)
    reader.onloadend = () => {
      this.setState({ buffer: Buffer(reader.result) })
      console.log('buffer', this.state.buffer)
    }
  }

  onSubmit = (event) => {
    event.preventDefault()
    console.log("Submitting file to ipfs...")
    ipfs.add(this.state.buffer, (error, result) => {
      console.log('Ipfs result', result)
      if(error) {
        console.error(error)
        return
      }
         return this.setState({ memeHash: result[0].hash })
    })
  }

  render() {
    return (
      <div class="top">
  <div class="wrapper">
    <header>File Uploader</header>
    <form onSubmit={this.onSubmit} class="inputs">
      <input class="file-input" type="file" id="file_input" accept="application/pdf" onChange={this.captureFile} />
      <i class="fas fa-cloud-upload-alt"></i>
      <p id="upload_fileName">Browse File to Upload</p>

    <section class="progress-area"></section>
    <section class="uploaded-area"></section>

    <div class="sub">
      <button type='submit' id='btn'>Upload</button>
    </div>
    </form>
  </div>
  <a
    href = {`https://ipfs.infura.io/ipfs/${this.state.memeHash}`}
    >
    Uploaded File
    </a>
</div>
    );
  }
}


export default App;
