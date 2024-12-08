//SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.10;

contract SmartProduct {
    uint idDigits = 16;
    // primeros dos digitos definen tipo
    Producto[] productos;
    mapping (uint => address) public productoAPropietario;
    mapping (address => uint) propietarioProductos;

    function _crearProducto(string memory _nombre, uint _id)
     private 
    {
        productos.push(Producto(_nombre, _id));
        emit NuevoProducto(_id, _nombre, _id);
    }

    function _generarIdAleatorio(string memory _str) private view
    returns (uint id) {
        uint rand = uint(keccak256(abi.encodePacked(_str)));
        return rand % (10 ** idDigits);
    }

    function crearProductoAleatorio(string memory _nombre) public 
    {
        uint256 randId = _generarIdAleatorio(_nombre);
        _crearProducto(_nombre, randId);
    }

    function Propiedad(uint _prodId) public {
        productoAPropietario[_prodId] = msg.sender;
        propietarioProductos[msg.sender] += 1;

    }

    function getProductosPorPropietario(address _propietario) view external 
    returns (uint[] memory) {
        uint contador = 0;
        uint[] memory resultado = new uint[](propietarioProductos[_propietario]);

        for (uint i = 0; i < productos.length; i++) {
            
            if (productoAPropietario[productos[i].id] == _propietario) {
                resultado[contador] = productos[i].id;
                contador++;
            }
        }

        return resultado;
    }

    event NuevoProducto(uint ArrayProductId, string nombre, uint id);
}

struct Producto {
    string nombre;
    uint id;
}

