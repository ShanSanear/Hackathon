using System;
using System.Collections.Generic;
using System.Linq;
using System;
using System.ComponentModel.DataAnnotations;

namespace HackathonBase.Models
{
    public class Entry
    {
        public int Id { get; set; }
        public float Average { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public int SourceDeviceId { get; set; }
    }
}
