﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using HackathonBase.Models;
using Microsoft.AspNetCore.Mvc;

namespace HackathonBase.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class DeviceController : Controller
    {
        private readonly EntryContext _context;

        public DeviceController(EntryContext context)
        {
            _context = context;
        }

        [HttpPost]
        public IActionResult Create(Device device)
        {
            if (device == null)
                return NoContent();

            _context.Add(device);
            _context.SaveChanges();

            return Ok();
        }


        [HttpPost]
        public IActionResult Create(IEnumerable<Device> devices)
        {
            if (devices == null || !devices.Any())
                return NoContent();
            
            foreach (var device in devices)
            {
                _context.Add(device);
            }

            _context.SaveChanges();

            return Ok();
        }


    }
}