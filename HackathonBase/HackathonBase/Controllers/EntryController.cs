using System;
using System.Collections;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using HackathonBase.Models;
using Microsoft.AspNetCore.Mvc;

namespace HackathonBase.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class EntryController : Controller
    {
        private readonly EntryContext _context;

        public EntryController(EntryContext context)
        {
            _context = context;
        }

        [HttpPost]
        public IActionResult Create(Entry entry)
        {
            if (entry == null)
                return NoContent();

            _context.Add(entry);
            _context.SaveChanges();

            return Ok();
        }
        
        [HttpPost]
        [Route("[action]")]
        public IActionResult Post([FromBody] Dates dates)
        {
            List<Entry> entries = _context.Entries.Where(
                x =>
                    DateTime.Compare(x.StartTime, dates.StartTime) >= 0 &&
                    DateTime.Compare(x.EndTime, dates.EndTime) <= 0).ToList();

            return Json(entries);
        }
    }

    public class Dates
    {
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
    }
}