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
        public IActionResult Create(IEnumerable<Entry> entries)
        {
            if (entries == null || !entries.Any())
                return NoContent();

            foreach (var entry in entries)
            {
                _context.Add(entry);
            }

            _context.SaveChanges();

            return Ok();
        }

        [HttpGet]
        public IActionResult Get(DateTime startTime, DateTime endTime)
        {
            List<Entry> entries = _context.Entries.Where(
                x =>
                    DateTime.Compare(x.StartTime, startTime) >= 0 &&
                    DateTime.Compare(x.EndTime, endTime) <= 0).ToList();

            return Json(entries);
        }
    }
}