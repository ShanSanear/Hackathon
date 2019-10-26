using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
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

            Device alreadyExistingDevice = _context.Devices.ToList().Find(x=>x.Name == device.Name);
            if (alreadyExistingDevice != null)
            {
                return Json(alreadyExistingDevice.Id);
            }

            _context.Update(device);
            _context.SaveChanges();

            return Json(device.Id);
        }


    }
}