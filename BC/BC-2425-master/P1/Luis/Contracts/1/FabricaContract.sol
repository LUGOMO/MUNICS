//SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.10;

contract SmartProduct {
    uint idDigits = 16;
    // primeros dos digitos definen tipo
    Producto[] productos;

    function crearProducto(string memory _nombre, uint _id) private 
    {
        productos.push(Producto(_nombre, _id));
        uint ArrayProductoId = productos.length - 1;
        emit NuevoProducto(ArrayProductoId ,_nombre ,_id);
    }

    function _generarIdAleatorio(string memory _str) private view
    returns (uint id) {
        uint rand = uint(keccak256(abi.encodePacked(_str)));
        return rand % (10**idDigits);
    }

    function crearProductoAleatorio(string memory _nombre) public
    {
        uint256 randID = _generarIdAleatorio(_nombre);   
        crearProducto(_nombre,randID);
    }
    event NuevoProducto(uint ArrayProductoId , string nombre , uint id);

    mapping (uint => address) public productoAPropietario;
    mapping (address => uint) propietarioProductos;

    function propiedad(uint productoId) public  
    {
        productoAPropietario[productoId] = msg.sender;
        propietarioProductos[msg.sender] += 1;
    }

    function getProductosPorPropietario (address _propietario) external view 
    returns (uint[] memory)
    {
        uint contador = 0;
        uint[] memory resultado = new uint[](propietarioProductos[_propietario]);
        {
        for (uint i = 0; i < productos.length; i++){
            if (productoAPropietario[productos[i].id] == _propietario)
            {
                resultado[contador] = productos[i].id;
                contador++;
            }
        }
        return resultado;
        }    
    }
struct Producto {
    string nombre;
    uint id;
}
}
